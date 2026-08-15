import type { Medication } from '../components/MedicationCard';

const INITIAL_MEDICATIONS: Medication[] = [
  {
    id: 'med_1',
    name: 'Albuterol Sulfate Inhaler',
    dose: '90 mcg (2 Puffs)',
    time: '08:00 AM',
    frequency: 'Every 4-6 hours as needed',
    instructions: 'Inhale 2 puffs for shortness of breath or persistent dry cough.',
    status: 'taken',
    startDate: '11 Aug 2026',
    duration: '14 Days',
    nextDose: '02:00 PM (Log as needed)'
  },
  {
    id: 'med_2',
    name: 'Amoxicillin Oral Capsule',
    dose: '500 mg (1 Capsule)',
    time: '09:00 AM',
    frequency: 'Three times daily',
    instructions: 'Take with food or water. Finish the entire course of medication.',
    status: 'upcoming',
    startDate: '12 Aug 2026',
    duration: '7 Days',
    nextDose: '02:00 PM'
  },
  {
    id: 'med_3',
    name: 'Guaifenesin Cough Relief',
    dose: '09:00 PM',
    time: '09:00 PM',
    frequency: 'Every 12 hours',
    instructions: 'Take with a full glass of water. Swallow whole; do not crush.',
    status: 'upcoming',
    startDate: '12 Aug 2026',
    duration: '5 Days',
    nextDose: '09:00 PM'
  },
  {
    id: 'med_4',
    name: 'Multivitamin Formula',
    dose: '1 Capsule',
    time: '07:30 AM',
    frequency: 'Once daily',
    instructions: 'Take in the morning with breakfast to support recovery.',
    status: 'taken',
    startDate: '01 Aug 2026',
    duration: 'Ongoing',
    nextDose: 'Tomorrow at 07:30 AM'
  }
];

export const medicationService = {
  getMedications(): Medication[] {
    const stored = localStorage.getItem('carepath_medications');
    if (!stored) {
      localStorage.setItem('carepath_medications', JSON.stringify(INITIAL_MEDICATIONS));
      return INITIAL_MEDICATIONS;
    }
    return JSON.parse(stored);
  },

  saveMedications(meds: Medication[]): void {
    localStorage.setItem('carepath_medications', JSON.stringify(meds));
  },

  markAsTaken(id: string): Medication[] {
    const meds = this.getMedications();
    const updated = meds.map(m => m.id === id ? { ...m, status: 'taken' as const } : m);
    this.saveMedications(updated);
    
    // Fire a local event to update components listening to changes
    window.dispatchEvent(new Event('medication_updated'));
    
    return updated;
  },

  getAdherenceSummary() {
    const meds = this.getMedications();
    const total = meds.length;
    const taken = meds.filter(m => m.status === 'taken').length;
    const missed = meds.filter(m => m.status === 'missed').length;
    
    // Simulate static totals for historical compliance calculation
    const historicalTotal = 24;
    const historicalTaken = 21;
    const historicalMissed = 3;
    
    const overallTaken = historicalTaken + taken;
    const overallTotal = historicalTotal + total;
    const percentage = Math.round((overallTaken / overallTotal) * 100);

    return {
      percentage,
      missed: historicalMissed + missed,
      taken: overallTaken,
      total: overallTotal
    };
  }
};
