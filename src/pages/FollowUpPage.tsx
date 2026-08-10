import { useEffect, useState } from 'react';
import { usePatient } from '../context/PatientContext';
import { followupService } from '../services/followupService';
import { 
  CheckCircle, 
  AlertCircle, 
  PlusCircle, 
  Activity,
  FileCheck
} from 'lucide-react';
import type { FollowUp } from '../types';

export default function FollowUpPage() {
  const { patient } = usePatient();
  const [followups, setFollowups] = useState<FollowUp[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // New check-in form state
  const [symptomsLogged, setSymptomsLogged] = useState('');
  const [notes, setNotes] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const fetchFollowups = async () => {
    if (!patient) return;
    setIsLoading(true);
    setError(null);
    try {
      if (patient.id === 'demo_patient_id') {
        setFollowups([
          {
            id: '1',
            patient_id: 'demo_patient_id',
            check_in_date: new Date(Date.now() - 86400000 * 3).toISOString(),
            status: 'completed',
            symptoms_logged: 'Dry cough persistent. No shortness of breath.',
            notes: 'Resting well, using inhaler occasionally.',
            created_at: new Date(Date.now() - 86400000 * 3).toISOString(),
          },
          {
            id: '2',
            patient_id: 'demo_patient_id',
            check_in_date: new Date().toISOString(),
            status: 'completed',
            symptoms_logged: 'Cough improved. Felt slight shortness of breath after climbing stairs.',
            notes: 'Scheduled Pulmonology appointment for next week.',
            created_at: new Date().toISOString(),
          }
        ]);
      } else {
        const data = await followupService.getFollowUps(patient.id);
        const sorted = [...data].sort((a, b) => 
          new Date(b.check_in_date).getTime() - new Date(a.check_in_date).getTime()
        );
        setFollowups(sorted);
      }
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Failed to fetch follow-ups. Ensure local API is active.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchFollowups();
  }, [patient]);

  const handleSubmitCheckin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!patient || !symptomsLogged) return;
    setIsSubmitting(true);
    setSuccessMsg(null);

    const payload = {
      patient_id: patient.id,
      check_in_date: new Date().toISOString(),
      symptoms_logged: symptomsLogged,
      notes: notes,
      status: 'completed' as const
    };

    try {
      if (patient.id === 'demo_patient_id') {
        const newLog: FollowUp = {
          id: String(followups.length + 1),
          created_at: new Date().toISOString(),
          ...payload
        };
        setFollowups(prev => [newLog, ...prev]);
      } else {
        await followupService.createFollowUp(payload);
        await fetchFollowups();
      }
      setSymptomsLogged('');
      setNotes('');
      setSuccessMsg('Check-in logged successfully.');
      setTimeout(() => setSuccessMsg(null), 3000);
    } catch (err: any) {
      console.error(err);
      alert(err.message || 'Failed to submit follow-up check-in.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-6">

      {successMsg && (
        <div className="bg-brand-sage-bg border border-brand-sage-text/10 text-brand-sage-text p-4 rounded-xl text-sm flex items-center gap-2">
          <CheckCircle className="w-5 h-5 shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      {error && (
        <div className="bg-brand-rose-bg border border-brand-rose-text/10 text-brand-rose-text p-4 rounded-xl text-sm flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5" />
            <span>{error}</span>
          </div>
          <button onClick={fetchFollowups} className="text-xs font-bold underline">Retry</button>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Form panel */}
        <div className="bg-brand-card border border-brand-slate/10 p-6 rounded-2xl shadow-sm md:col-span-1 h-fit">
          <h3 className="font-display font-semibold text-sm text-brand-plum mb-4 flex items-center gap-2">
            <PlusCircle className="w-4 h-4 text-brand-lavender" />
            How are you doing?
          </h3>

          <form onSubmit={handleSubmitCheckin} className="flex flex-col gap-4">
            <div className="flex flex-col gap-1">
              <label className="text-xxs font-semibold text-brand-slate">Active Symptoms Today</label>
              <textarea
                rows={3}
                placeholder="Log cough, breathing, congestion, fatigue..."
                value={symptomsLogged}
                onChange={(e) => setSymptomsLogged(e.target.value)}
                className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-3 py-2.5 text-xs focus:border-brand-lavender focus:ring-1 focus:ring-brand-lavender outline-none resize-none transition-all"
                required
              />
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xxs font-semibold text-brand-slate">Notes / Updates</label>
              <textarea
                rows={3}
                placeholder="e.g. Appointment scheduled, rested well, inhaler doses..."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-3 py-2.5 text-xs focus:border-brand-lavender focus:ring-1 focus:ring-brand-lavender outline-none resize-none transition-all"
              />
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="bg-brand-lavender hover:bg-brand-lavender-hover text-white text-xs font-semibold py-2.5 rounded-xl transition-all shadow-sm flex items-center justify-center cursor-pointer"
            >
              Submit Check-in
            </button>
          </form>
        </div>

        {/* History panel */}
        <div className="bg-brand-card border border-brand-slate/10 p-6 rounded-2xl shadow-sm md:col-span-2">
          <h3 className="font-display font-semibold text-sm text-brand-plum mb-6 flex items-center gap-2">
            <Activity className="w-4 h-4 text-brand-lavender" />
            Follow-up History Logs
          </h3>

          {isLoading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-lavender"></div>
            </div>
          ) : followups.length === 0 ? (
            <div className="text-center py-10 flex flex-col items-center gap-3">
              <FileCheck className="w-8 h-8 text-brand-slate/40" />
              <p className="text-xs text-brand-slate">No check-ins logged yet. Keep your path updated.</p>
            </div>
          ) : (
            <div className="flex flex-col gap-5">
              {followups.map((log) => (
                <div key={log.id} className="border-b border-brand-slate/10 pb-4 last:border-0 last:pb-0">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-xxs font-bold text-brand-sage-text bg-brand-sage-bg px-2.5 py-0.5 rounded-full">
                      Logged Check-in
                    </span>
                    <span className="text-xxs text-brand-slate/75">
                      {new Date(log.check_in_date).toLocaleDateString(undefined, { 
                        month: 'short', 
                        day: 'numeric',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  </div>

                  <div className="flex flex-col gap-2 pl-1">
                    <div>
                      <span className="text-xxs font-bold text-brand-slate uppercase block">Symptoms Status</span>
                      <p className="text-xs text-brand-plum leading-relaxed font-light mt-0.5">
                        {log.symptoms_logged}
                      </p>
                    </div>

                    {log.notes && (
                      <div>
                        <span className="text-xxs font-bold text-brand-slate uppercase block">Additional Notes</span>
                        <p className="text-xs text-brand-slate leading-relaxed font-light mt-0.5 italic">
                          {log.notes}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
