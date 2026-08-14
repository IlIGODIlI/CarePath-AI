export interface DoctorQuestion {
  id: string;
  text: string;
  relevance: string;
  isAsked: boolean;
  isCustom?: boolean;
}

export interface DoctorReview {
  isReviewed: boolean;
  reviewedBy: string;
  reviewedDate: string;
  recommendation: string; // Confirm or Modify
  originalRecommendation: string;
  modifiedSpecialist?: string;
  doctorNote: string;
  doctorRecommendations: string[];
  followUpDate: string;
}

const INITIAL_QUESTIONS: DoctorQuestion[] = [
  {
    id: 'q_1',
    text: 'My dry cough has persisted for over 3 days without improvement. Does this suggest a bacterial trigger or bronchitis?',
    relevance: 'Evaluating symptom duration helps distinguish temporary viral irritation from acute lower respiratory tract triggers.',
    isAsked: false
  },
  {
    id: 'q_2',
    text: 'My chest X-ray reports minor lower lobe consolidation. What does this consolidate indicating for my recovery timeline?',
    relevance: 'Discussing imaging density parameters clarifies if targeted pulmonary care or antibiotics are warranted.',
    isAsked: false
  },
  {
    id: 'q_3',
    text: 'The Albuterol bronchodilator treatment has not resolved my shortness of breath. Should we evaluate alternative routing?',
    relevance: 'Determining bronchodilator efficacy informs the doctor whether to step up controller therapies or switch agent classes.',
    isAsked: false
  }
];

export const doctorBridgeService = {
  getQuestions(): DoctorQuestion[] {
    const stored = localStorage.getItem('carepath_doctor_questions');
    if (!stored) {
      localStorage.setItem('carepath_doctor_questions', JSON.stringify(INITIAL_QUESTIONS));
      return INITIAL_QUESTIONS;
    }
    return JSON.parse(stored);
  },

  saveQuestions(questions: DoctorQuestion[]): void {
    localStorage.setItem('carepath_doctor_questions', JSON.stringify(questions));
  },

  addQuestion(text: string): DoctorQuestion[] {
    const questions = this.getQuestions();
    const newQuestion: DoctorQuestion = {
      id: `q_custom_${Date.now()}`,
      text,
      relevance: 'Custom patient-added discussion point.',
      isAsked: false,
      isCustom: true
    };
    const updated = [...questions, newQuestion];
    this.saveQuestions(updated);
    return updated;
  },

  toggleQuestionAsked(id: string): DoctorQuestion[] {
    const questions = this.getQuestions();
    const updated = questions.map(q => q.id === id ? { ...q, isAsked: !q.isAsked } : q);
    this.saveQuestions(updated);
    return updated;
  },

  getReview(): DoctorReview | null {
    const stored = localStorage.getItem('carepath_doctor_review');
    return stored ? JSON.parse(stored) : null;
  },

  submitReview(review: DoctorReview): void {
    localStorage.setItem('carepath_doctor_review', JSON.stringify(review));
    window.dispatchEvent(new Event('doctor_review_updated'));
  },

  resetReview(): void {
    localStorage.removeItem('carepath_doctor_review');
    localStorage.setItem('carepath_doctor_questions', JSON.stringify(INITIAL_QUESTIONS));
    window.dispatchEvent(new Event('doctor_review_updated'));
  }
};
