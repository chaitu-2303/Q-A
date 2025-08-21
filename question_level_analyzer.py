from typing import List, Dict, Any
import logging

class QuestionLevelAnalyzer:
    """Analyzes question difficulty levels based on various factors"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Complexity indicators
        self.complex_indicators = {
            'advanced': [
                'విశ్లేషించండి', 'వివరించండి', 'తులనా చేయండి', 'కారణాలు', 'ప్రభావం',
                'పరిణామం', 'సిద్ధాంతం', 'సూత్రం', 'ప్రక్రియ', 'విధానం'
            ],
            'intermediate': [
                'ఎందుకు', 'ఎలా', 'ఏ విధంగా', 'ఏ కారణంగా', 'ప్రధాన', 'ముఖ్యమైన',
                'విశేషం', 'ప్రత్యేకం', 'విలక్షణం'
            ],
            'basic': [
                'ఎవరు', 'ఏమిటి', 'ఎక్కడ', 'ఎప్పుడు', 'ఎంత', 'ఏం', 'ఎవరి'
            ]
        }
        
        # Sentence complexity factors
        self.complexity_factors: Dict[str, Dict[str, Any]] = {
            'sentence_length': {
                'basic': (0, 15),
                'intermediate': (15, 30),
                'advanced': (30, float('inf'))
            },
            'word_complexity': {
                'basic': ['చిన్న', 'పెద్ద', 'మంచి', 'చెడు', 'కొత్త', 'పాత'],
                'intermediate': ['ముఖ్యమైన', 'ప్రత్యేకమైన', 'విలక్షణమైన', 'అద్భుతమైన'],
                'advanced': ['అసాధారణమైన', 'అద్వితీయమైన', 'అపూర్వమైన', 'అసమానమైన']
            }
        }
    
    def analyze_question_level(self, question: str, answer: str, context: str) -> Dict[str, Any]:
        """Analyze the difficulty level of a question based on multiple factors"""
        
        level_scores = {
            'basic': 0,
            'intermediate': 0,
            'advanced': 0
        }
        
        # Factor 1: Question complexity indicators
        question_lower = question.lower()
        for level, indicators in self.complex_indicators.items():
            for indicator in indicators:
                if indicator.lower() in question_lower:
                    level_scores[level] += 2
        
        # Factor 2: Answer complexity
        answer_words = answer.split()
        answer_length = len(answer_words)
        
        for level, (min_len, max_len) in self.complexity_factors['sentence_length'].items():
            if min_len <= answer_length < max_len:
                level_scores[level] += 1
        
        # Factor 3: Word complexity in answer
        for level, words in self.complexity_factors['word_complexity'].items():
            for word in words:
                if word in answer:
                    level_scores[level] += 1
        
        # Factor 4: Question length
        question_length = len(question.split())
        if question_length <= 5:
            level_scores['basic'] += 1
        elif question_length <= 10:
            level_scores['intermediate'] += 1
        else:
            level_scores['advanced'] += 1
        
        # Determine final level
        max_score = max(level_scores.values())
        final_level = [level for level, score in level_scores.items() if score == max_score][0]
        
        # Calculate confidence score
        total_score = sum(level_scores.values())
        confidence = min(max_score / total_score if total_score > 0 else 0, 1.0)
        
        return {
            'level': final_level,
            'confidence': round(confidence, 2),
            'scores': level_scores,
            'factors': {
                'question_length': question_length,
                'answer_length': answer_length,
                'complex_indicators': [ind for inds in self.complex_indicators.values() 
                                     for ind in inds if ind.lower() in question_lower]
            }
        }
    
    def categorize_questions_by_level(self, qa_pairs: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize questions by their difficulty levels"""
        categorized: Dict[str, List[Dict[str, Any]]] = {
            'basic': [],
            'intermediate': [],
            'advanced': []
        }
        
        for qa in qa_pairs:
            level_info = self.analyze_question_level(
                qa['question'], 
                qa['answer'], 
                qa.get('context', '')
            )
            qa_with_level = {**qa, **level_info}
            categorized[level_info['level']].append(qa_with_level)
        
        return categorized
    
    def get_level_statistics(self, qa_pairs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about question levels"""
        categorized = self.categorize_questions_by_level(qa_pairs)
        
        stats: Dict[str, Any] = {
            'total_questions': len(qa_pairs),
            'level_distribution': {
                level: len(questions) 
                for level, questions in categorized.items()
            },
            'percentage_distribution': {},
            'average_confidence': 0
        }
        
        # Calculate percentages
        total = stats['total_questions']
        for level, count in stats['level_distribution'].items():
            stats['percentage_distribution'][level] = round((count / total * 100), 1) if total > 0 else 0
        
        # Calculate average confidence
        confidences: List[float] = []
        for questions in categorized.values():
            for q in questions:
                confidences.append(q.get('confidence', 0))
        
        stats['average_confidence'] = round(sum(confidences) / len(confidences), 2) if confidences else 0
        
        return stats
