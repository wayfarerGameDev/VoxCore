import re
from rapidfuzz import process, fuzz

class ServiceIntentRapidFuzz:
    command = "--service_intent_rapidfuzz"
    
    def __init__(self, command_router_function):
        self.route_command = command_router_function
        self._rules = []
        self._intents_parsed = {} 
        self.threshold = 80

    def start(self):
        self.route_command("--ui_header Service added: Intent_Rapidfuzz")
    
    def stop(self):
        self.route_command("--ui_notify Service removed: Intent_Rapidfuzz")
        self._rules.clear()
        self._intents_parsed.clear()
    
    def on_command(self, text: str) -> bool:
        # Intent: Add
        if text.startswith("--intent_add "):
            sentence = text[13:].strip()
            if sentence:
                self._rules.append(sentence)
                self._parse_rules()
                self.route_command(f"--ui_notify Intent added: '{sentence}'")
            return True
        
        # Intent: Remove
        if text.startswith("--intent_remove "):
            sentence = text[16:].strip()
            if sentence in self._rules:
                self._rules.remove(sentence)
                self._parse_rules()
                self.route_command(f"--ui_notify Intent removed: '{sentence}'")
            return True

        # Guard: Ignore system commands
        if text.startswith("--"): 
            return False

        # Clean user input (lowercase, strip weird punctuation)
        user_input = text.translate(str.maketrans('', '', ".,!?;:()[]{}'\"\\")).lower().strip()
        
        # Execute Fuzzy Match
        trigger_phrases = list(self._intents_parsed.keys())
        
        # Finds the best match. Returns a tuple: (matched_string, score, index)
        best_match = process.extractOne(user_input, trigger_phrases, scorer=fuzz.token_set_ratio)
        if best_match:
            matched_phrase, score, _ = best_match
            if score >= self.threshold:
                final_command = self._intents_parsed[matched_phrase]
                self.route_command(f"--ui_notify [Intent Matched] ({score}% confidence): {final_command}")
                self.route_command(final_command)
                return True

        return False

    def _parse_rules(self):
        self._intents_parsed.clear()
        
        pattern = re.compile(r"""
        # The Condition (when, if, every time, anytime, once)
        (?:when(?:ever)?|if|every\s*time|anytime|once|as\s*soon\s*as)\s+

        # The Subject (I, we, you, the user)
        (?:I|we|you|they|the\s*user)\s+
    
        # The Trigger Action (say, type, enter, tell you to, ask for, etc.)
        (?:say|type|enter|input|write|speak|command|tell\s*you(?:\s*to)?|ask(?:\s*for)?|prompt)\s+
    
        # Capture Trigger Phrases (ignores optional quotes)
        ['"]?(.*?)['"]?
    
        # Optional Separators & Politeness (then, comma, please, just)
        \s*(?:,|\bthen\b|\bthan\b|please|just|go\s*ahead\s*and)?\s*
    
        # The Result Action (output, run, execute, print, respond with, etc.)
        (?:output|run|say|type|do|execute|print|return|show(?:\s*me)?|give(?:\s*me)?|respond(?:\s*with)?|reply(?:\s*with)?|make)\s+
    
        # Group 2: The Command/Output (ignores optional quotes)
        ['"]?(.*?)['"]?
    
        # End punctuation
        [\.\!\?]*$
        """, re.IGNORECASE | re.VERBOSE)
        
        
        for rule in self._rules:
            match = pattern.search(rule)
            if match:
                raw_triggers = match.group(1).lower().strip()
                command = match.group(2).strip()
                
                # Split the phrase by commas OR the word "or"
                trigger_list = [t.strip() for t in re.split(r',\s*|\s+or\s+', raw_triggers)]
                
                # Add each trigger to the dictionary separately
                for trigger in trigger_list:
                    self._intents_parsed[trigger] = command