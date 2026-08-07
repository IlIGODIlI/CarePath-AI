import React, { useState, useEffect } from 'react';
import { usePatient } from '../context/PatientContext';
import { AlertCircle, CheckCircle2, User, Save } from 'lucide-react';

export default function ProfilePage() {
  const { patient, updatePatientProfile, isLoading, error } = usePatient();
  
  const [name, setName] = useState('');
  const [age, setAge] = useState<number>(30);
  const [gender, setGender] = useState('Male');
  const [bloodType, setBloodType] = useState('O+');
  const [allergiesInput, setAllergiesInput] = useState('');
  const [medicalHistory, setMedicalHistory] = useState('');
  const [currentSymptoms, setCurrentSymptoms] = useState('');
  
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Sync state with patient context
  useEffect(() => {
    if (patient) {
      setName(patient.name || '');
      setAge(patient.age || 30);
      setGender(patient.gender || 'Male');
      setBloodType(patient.blood_type || 'O+');
      setAllergiesInput(patient.allergies?.join(', ') || '');
      setMedicalHistory(patient.medical_history || '');
      setCurrentSymptoms(patient.current_symptoms || '');
    }
  }, [patient]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccessMessage(null);

    const allergies = allergiesInput
      .split(',')
      .map((item) => item.trim())
      .filter((item) => item.length > 0);

    try {
      await updatePatientProfile({
        name,
        age: Number(age),
        gender,
        blood_type: bloodType,
        allergies,
        medical_history: medicalHistory,
        current_symptoms: currentSymptoms,
      });
      setSuccessMessage('Patient context updated successfully.');
      setTimeout(() => setSuccessMessage(null), 4000);
    } catch (err) {
      console.error('Failed to update patient profile:', err);
    }
  };

  return (
    <div className="max-w-3xl mx-auto flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-bold tracking-tight text-brand-plum">Patient Context</h1>
        <p className="text-brand-slate text-sm">
          Keep your medical history and current status updated to help CarePath provide accurate specialist routing.
        </p>
      </div>

      {successMessage && (
        <div className="bg-brand-sage-bg border border-brand-sage-text/10 text-brand-sage-text p-4 rounded-xl text-sm flex items-center gap-2.5 shadow-sm">
          <CheckCircle2 className="w-5 h-5 shrink-0" />
          <span>{successMessage}</span>
        </div>
      )}

      {error && (
        <div className="bg-brand-rose-bg border border-brand-rose-text/10 text-brand-rose-text p-4 rounded-xl text-sm flex items-center gap-2.5 shadow-sm">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-brand-card border border-brand-slate/10 p-6 md:p-8 rounded-2xl shadow-sm flex flex-col gap-6">
        {/* Core demographic information */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex flex-col gap-1.5 md:col-span-2">
            <label className="text-xs font-semibold text-brand-slate px-0.5">Full Name</label>
            <div className="relative">
              <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-brand-slate" />
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl pl-10 pr-4 py-3 text-sm focus:border-brand-lavender focus:ring-1 focus:ring-brand-lavender outline-none transition-all"
                required
              />
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-brand-slate px-0.5">Age</label>
            <input
              type="number"
              value={age}
              onChange={(e) => setAge(Number(e.target.value))}
              min="0"
              max="130"
              className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-4 py-3 text-sm focus:border-brand-lavender focus:ring-1 focus:ring-brand-lavender outline-none transition-all"
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-brand-slate px-0.5">Gender</label>
            <select
              value={gender}
              onChange={(e) => setGender(e.target.value)}
              className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-4 py-3 text-sm focus:border-brand-lavender focus:ring-1 focus:ring-brand-lavender outline-none transition-all"
            >
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
              <option value="Prefer not to say">Prefer not to say</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-brand-slate px-0.5">Blood Type</label>
            <input
              type="text"
              placeholder="e.g. O+, A-"
              value={bloodType}
              onChange={(e) => setBloodType(e.target.value)}
              className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-4 py-3 text-sm focus:border-brand-lavender focus:ring-1 focus:ring-brand-lavender outline-none transition-all"
            />
          </div>
        </div>

        {/* Medical details fields */}
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-semibold text-brand-slate px-0.5">Allergies (comma-separated)</label>
          <input
            type="text"
            placeholder="e.g. Penicillin, Peanuts, Pollen"
            value={allergiesInput}
            onChange={(e) => setAllergiesInput(e.target.value)}
            className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-4 py-3 text-sm focus:border-brand-lavender focus:ring-1 focus:ring-brand-lavender outline-none transition-all"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-semibold text-brand-slate px-0.5">Medical History Summary</label>
          <textarea
            rows={3}
            placeholder="Brief description of past surgeries, chronic illnesses, active medications..."
            value={medicalHistory}
            onChange={(e) => setMedicalHistory(e.target.value)}
            className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-4 py-3 text-sm focus:border-brand-lavender focus:ring-1 focus:ring-brand-lavender outline-none transition-all resize-none"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-semibold text-brand-slate px-0.5">Active Symptoms & Concerns</label>
          <textarea
            rows={4}
            placeholder="How are you feeling? Detail symptoms, onset, severity, what triggers them..."
            value={currentSymptoms}
            onChange={(e) => setCurrentSymptoms(e.target.value)}
            className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-4 py-3 text-sm focus:border-brand-lavender focus:ring-1 focus:ring-brand-lavender outline-none transition-all resize-none"
          />
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={isLoading}
          className="bg-brand-lavender hover:bg-brand-lavender-hover disabled:bg-brand-lavender/50 text-white font-semibold text-sm py-3 rounded-xl transition-all shadow-sm flex items-center justify-center gap-2 mt-4 cursor-pointer"
        >
          {isLoading ? 'Saving Changes...' : 'Save Patient Context'}
          <Save className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
