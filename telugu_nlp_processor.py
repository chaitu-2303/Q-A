import re
from typing import List, Dict, Any
import logging
from question_level_analyzer import QuestionLevelAnalyzer

class TeluguNLPProcessor:
    """Advanced Telugu NLP processor for Q&A generation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.level_analyzer = QuestionLevelAnalyzer()
        
        # Telugu question patterns
        self.question_patterns = {
            'who': ['ఎవరు', 'ఎవరి', 'ఎవరిని', 'ఎవరి ద్వారా'],
            'what': ['ఏమిటి', 'ఏమి', 'ఏది', 'ఏం'],
            'when': ['ఎప్పుడు', 'ఏ సమయంలో', 'ఏ కాలంలో'],
            'where': ['ఎక్కడ', 'ఏ ప్రదేశంలో', 'ఏ చోట'],
            'why': ['ఎందుకు', 'ఏ కారణంగా', 'ఎందుకంటే'],
            'how': ['ఎలా', 'ఏ విధంగా', 'ఏ విధంగా']
        }
        
        # Telugu sentence endings
        self.sentence_endings = ['.', '!', '?', '।', '॥']
        
        # Common Telugu words for analysis
        self.common_verbs = ['చేశాడు', 'చేశారు', 'చేసింది', 'ఉంది', 'ఉన్నాడు', 'వచ్చాడు', 'పోయాడు']
        self.common_nouns = ['వ్యక్తి', 'స్థలం', 'సమయం', 'విషయం', 'పని', 'ఘటన']
    
    def split_sentences(self, text: str) -> List[str]:
        """Split Telugu text into sentences"""
        # Split by sentence endings
        pattern = '|'.join(map(re.escape, self.sentence_endings))
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]
    
    def extract_entities(self, sentence: str) -> Dict[str, List[str]]:
        """Extract entities from Telugu sentence"""
        entities: Dict[str, List[str]] = {
            'persons': [],
            'locations': [],
            'dates': [],
            'organizations': []
        }
        
        # Simple entity extraction based on patterns
        # Persons (looking for names ending with specific patterns)
        person_patterns = [
            r'(\w+రావు)',  # Names ending with రావు
            r'(\w+కుమార్)',  # Names ending with కుమార్
            r'(\w+దేవి)',  # Names ending with దేవి
        ]
        
        for pattern in person_patterns:
            matches = re.findall(pattern, sentence)
            entities['persons'].extend(matches)
        
        # Locations (looking for common location indicators)
        location_indicators = ['నగరం', 'పల్లె', 'గ్రామం', 'పట్టణం', 'రాష్ట్రం']
        for indicator in location_indicators:
            if indicator in sentence:
                # Extract word before the indicator
                match = re.search(r'(\w+)' + indicator, sentence)
                if match:
                    entities['locations'].append(match.group(1) + indicator)
        
        # Dates (simple patterns)
        date_patterns = [
            r'\d{4}',  # Years
            r'\d{1,2}వ తేదీ',  # Dates
            r'\w+ మాసం',  # Months
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, sentence)
            entities['dates'].extend(matches)
        
        return entities
    
    def generate_question_from_sentence(self, sentence: str, entities: Dict[str, List[str]]) -> List[Dict[str, str]]:
        """Generate a variety of intelligent questions from a sentence."""
        questions: List[Dict[str, str]] = []
        
        # Generate WHO questions
        if entities['persons']:
            for person in entities['persons']:
                # Replace person's name with "ఎవరు" to form a question
                question_text = sentence.replace(person, 'ఎవరు', 1) + "?"
                questions.append({'question': question_text, 'answer': person, 'type': 'who'})

        # Generate WHERE questions
        if entities['locations']:
            for location in entities['locations']:
                question_text = sentence.replace(location, 'ఎక్కడ', 1) + "?"
                questions.append({'question': question_text, 'answer': location, 'type': 'where'})

        # Generate WHEN questions
        if entities['dates']:
            for date in entities['dates']:
                question_text = sentence.replace(date, 'ఎప్పుడు', 1) + "?"
                questions.append({'question': question_text, 'answer': date, 'type': 'when'})

        # Generate WHY questions based on keywords
        why_keywords = ['కారణంగా', 'వల్ల', 'ఎందుకంటే']
        if any(keyword in sentence for keyword in why_keywords):
            # Attempt to find the clause before the keyword
            for keyword in why_keywords:
                if keyword in sentence:
                    parts = sentence.split(keyword)
                    if len(parts) > 1:
                        question_text = f"{parts[1].strip()}కి కారణం ఏమిటి?"
                        questions.append({'question': question_text, 'answer': parts[0].strip(), 'type': 'why'})
                        break

        # Generate HOW questions based on keywords
        how_keywords = ['విధంగా', 'ద్వారా']
        if any(keyword in sentence for keyword in how_keywords):
            for keyword in how_keywords:
                if keyword in sentence:
                    parts = sentence.split(keyword)
                    if len(parts) > 1:
                        question_text = f"{parts[0].strip()} ఎలా జరిగింది?"
                        questions.append({'question': question_text, 'answer': f"{keyword}{parts[1].strip()}", 'type': 'how'})
                        break
        
        # Fallback to a generic WHAT question if no other types are generated
        if not questions:
            questions.append({
                'question': f"'{sentence}' గురించి వివరించండి.",
                'answer': sentence,
                'type': 'what'
            })
            
        return questions
    
    def generate_qa_pairs(self, paragraph: str, num_questions: int = 5, difficulty: str = 'mixed') -> List[Dict[str, Any]]:
        """Generate Q&A pairs from Telugu paragraph"""
        try:
            # Split paragraph into sentences
            sentences = self.split_sentences(paragraph)
            
            qa_pairs: List[Dict[str, Any]] = []
            
            for sentence in sentences:
                if len(sentence) < 10:  # Skip very short sentences
                    continue
                
                # Extract entities
                entities = self.extract_entities(sentence)
                
                # Generate questions
                questions = self.generate_question_from_sentence(sentence, entities)
                
                # Add context to each question
                for q in questions:
                    q['context'] = sentence
                
                # Add to Q&A pairs
                qa_pairs.extend(questions)
            
            # Remove duplicates
            unique_qa: List[Dict[str, Any]] = []
            seen: set[str] = set()
            for qa in qa_pairs:
                key = qa['question']
                if key not in seen:
                    seen.add(key)
                    unique_qa.append(qa)
            
            # Analyze question levels
            qa_with_levels: List[Dict[str, Any]] = []
            for qa in unique_qa:
                level_info = self.level_analyzer.analyze_question_level(
                    qa['question'], 
                    qa['answer'], 
                    qa.get('context', '')
                )
                qa_with_level = {**qa, **level_info}
                qa_with_levels.append(qa_with_level)
            
            # Filter by difficulty
            if difficulty != 'mixed':
                qa_with_levels = [qa for qa in qa_with_levels if qa.get('level') == difficulty]
            
            # Limit number of questions
            num_questions = int(num_questions)
            
            # If not enough questions, add more generic ones to meet the count
            generic_question_templates = [
                ("'{sentence}' గురించి వివరించండి.", 'what'),
                ("'{sentence}' వాక్యం ఎలా ముగుస్తుంది?", 'how'),
                ("'{sentence}' వాక్యం యొక్క ప్రాముఖ్యత ఏమిటి?", 'why')
            ]
            
            while len(qa_with_levels) < num_questions and sentences:
                # Cycle through sentences and templates to generate varied generic questions
                sentence_index = len(qa_with_levels) % len(sentences)
                template_index = len(qa_with_levels) % len(generic_question_templates)
                
                sentence = sentences[sentence_index]
                template, q_type = generic_question_templates[template_index]
                
                question_text = template.format(sentence=sentence)
                
                if question_text not in seen:
                    generic_question = {
                        'question': question_text,
                        'answer': sentence,
                        'type': q_type,
                        'context': sentence
                    }
                    
                    level_info = self.level_analyzer.analyze_question_level(
                        generic_question['question'], 
                        generic_question['answer'], 
                        generic_question.get('context', '')
                    )
                    qa_with_level: Dict[str, Any] = {**generic_question, **level_info}
                    qa_with_levels.append(qa_with_level)
                    seen.add(question_text)
                else:
                    # If we've exhausted all unique combinations, we may have to stop to avoid infinite loops
                    # Or add a simple counter to the question to make it unique
                    question_text_unique = f"{question_text} ({len(qa_with_levels)})"
                    if question_text_unique not in seen:
                         generic_question = {
                            'question': question_text_unique,
                            'answer': sentence,
                            'type': q_type,
                            'context': sentence
                        }
                         level_info = self.level_analyzer.analyze_question_level(
                            generic_question['question'], 
                            generic_question['answer'], 
                            generic_question.get('context', '')
                        )
                         qa_with_level: Dict[str, Any] = {**generic_question, **level_info}
                         qa_with_levels.append(qa_with_level)
                         seen.add(question_text_unique)
                    else:
                        break # Break the loop if we can't generate a unique question

            return qa_with_levels[:num_questions]
            
        except Exception as e:
            self.logger.error(f"Error generating Q&A: {str(e)}")
            return []
    
    def validate_telugu_text(self, text: str) -> bool:
        """Validate if text contains Telugu characters"""
        telugu_pattern = r'[\u0C00-\u0C7F]+'
        return bool(re.search(telugu_pattern, text))

    def get_question_statistics(self, qa_pairs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get comprehensive statistics about generated questions"""
        return self.level_analyzer.get_level_statistics(qa_pairs)
