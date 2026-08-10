import { useEffect, useState } from 'react';
import { usePatient } from '../context/PatientContext';
import { analysisService } from '../services/analysisService';
import { Link } from 'react-router-dom';
import { 
  AlertTriangle, 
  Users2, 
  ArrowLeft, 
  FileText,
  Bookmark,
  CalendarCheck
} from 'lucide-react';
import type { AnalysisResult } from '../types';

export default function RecommendationPage() {
  const { patient } = usePatient();
  const [latestAnalysis, setLatestAnalysis] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadAnalysis = async () => {
      if (!patient) return;
      setIsLoading(true);
      setError(null);

      try {
        if (patient.id === 'demo_patient_id') {
          // Demo mock results
          setLatestAnalysis({
            id: 'demo_analysis',
            patient_id: 'demo_patient_id',
            status: 'completed',
            specialist_recommendation: 'Pulmonologist',
            explanation: 'Based on your persistent cough and mild shortness of breath alongside chest X-ray findings, a consultation with a pulmonologist is recommended to assess respiratory function.',
            considered_factors: [
              'Dry cough lasting 3 days', 
              'Chest X-ray report uploaded', 
              'Mild exertion-induced shortness of breath'
            ],
            safety_alerts: [
              'If chest pain, severe shortness of breath, or high fever develops, seek emergency care immediately.'
            ],
            created_at: new Date().toISOString(),
          });
        } else {
          // Real backend fetch
          const history = await analysisService.getAnalysisHistory(patient.id);
          if (history && history.length > 0) {
            const sorted = [...history].sort((a, b) => 
              new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
            );
            setLatestAnalysis(sorted[0]);
          } else {
            setLatestAnalysis(null);
          }
        }
      } catch (err: any) {
        console.error('Error fetching analysis:', err);
        setError(err.message || 'Failed to retrieve analysis results. Verify API is running.');
      } finally {
        setIsLoading(false);
      }
    };

    loadAnalysis();
  }, [patient]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-brand-lavender mb-4"></div>
        <p className="text-brand-slate text-sm">Retrieving your analysis report...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-brand-rose-bg border border-brand-rose-text/10 text-brand-rose-text p-6 rounded-2xl flex flex-col gap-4 max-w-2xl mx-auto my-10">
        <div className="flex items-center gap-3">
          <AlertTriangle className="w-6 h-6 shrink-0" />
          <h3 className="font-display font-semibold text-lg font-bold">Analysis Error</h3>
        </div>
        <p className="text-sm">{error}</p>
        <Link 
          to="/upload" 
          className="bg-brand-rose-text text-white text-xs font-semibold px-4 py-2.5 rounded-xl w-fit"
        >
          Return to Uploads
        </Link>
      </div>
    );
  }

  if (!latestAnalysis) {
    return (
      <div className="bg-brand-card border border-brand-slate/10 p-12 rounded-2xl max-w-xl mx-auto text-center flex flex-col items-center gap-6 my-10">
        <div className="w-14 h-14 bg-brand-bg rounded-full flex items-center justify-center text-brand-slate">
          <FileText className="w-6 h-6" />
        </div>
        <div>
          <h2 className="font-display text-xl font-bold text-brand-plum mb-2">No active analysis reports found</h2>
          <p className="text-brand-slate text-xs max-w-xs leading-relaxed mx-auto">
            You need to upload medical documents and trigger the clinical reasoning mapping before viewing results.
          </p>
        </div>
        <Link 
          to="/upload" 
          className="bg-brand-lavender hover:bg-brand-lavender-hover text-white text-xs font-semibold px-6 py-3 rounded-xl transition-all shadow-sm"
        >
          Go to Upload Center
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-6">
      {/* Back button and title badge */}
      <div className="flex items-center gap-3">
        <Link 
          to="/dashboard" 
          className="p-2 rounded-lg bg-brand-card border border-brand-slate/10 text-brand-slate hover:text-brand-plum transition-all cursor-pointer"
          title="Back to Dashboard"
          aria-label="Back to Dashboard"
        >
          <ArrowLeft className="w-4 h-4" />
        </Link>
        <span className="text-xxs font-bold text-brand-lavender uppercase tracking-wider bg-brand-lavender-light px-2.5 py-1 rounded-full">
          Analysis Report
        </span>
      </div>

      {/* Specialist Recommendation Block */}
      <div className="bg-brand-card border border-brand-slate/10 p-6 md:p-8 rounded-2xl shadow-sm flex flex-col md:flex-row gap-6 items-start">
        <div className="w-12 h-12 rounded-xl bg-brand-lavender-light text-brand-lavender flex items-center justify-center shrink-0">
          <Users2 className="w-6 h-6" />
        </div>
        <div className="flex-1 flex flex-col gap-2">
          <span className="text-xxs font-bold text-brand-slate uppercase tracking-wider">Recommended Next Step</span>
          <h2 className="font-display text-xl font-bold text-brand-plum">
            Consult a {latestAnalysis.specialist_recommendation}
          </h2>
          <p className="text-brand-slate text-sm font-light leading-relaxed">
            {latestAnalysis.explanation}
          </p>
        </div>
      </div>

      {/* Rationale and considered factors */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-brand-card border border-brand-slate/10 p-6 rounded-2xl shadow-sm">
          <h3 className="font-display text-sm font-bold text-brand-plum mb-4 flex items-center gap-2">
            <Bookmark className="w-4 h-4 text-brand-lavender" />
            Considered Clinical Factors
          </h3>
          <ul className="flex flex-col gap-3">
            {latestAnalysis.considered_factors?.map((factor, idx) => (
              <li key={idx} className="flex gap-3 items-start text-xs text-brand-plum font-light">
                <span className="w-5 h-5 rounded-full bg-brand-bg text-brand-slate font-bold flex items-center justify-center shrink-0 text-xxs">
                  {idx + 1}
                </span>
                <span className="pt-0.5">{factor}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Safety Block */}
        <div className="bg-brand-card border border-brand-slate/10 p-6 rounded-2xl shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="font-display text-sm font-bold text-brand-plum mb-4 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-brand-rose-text" />
              Safety Assessment
            </h3>
            
            {latestAnalysis.safety_alerts && latestAnalysis.safety_alerts.length > 0 ? (
              <div className="bg-brand-rose-bg border border-brand-rose-text/10 text-brand-rose-text p-4 rounded-xl text-xs leading-relaxed font-light mb-4">
                {latestAnalysis.safety_alerts[0]}
              </div>
            ) : (
              <p className="text-xs text-brand-slate leading-relaxed font-light mb-4">
                No immediate red-flag triggers identified in patient reports or demographics.
              </p>
            )}
          </div>

          <div className="text-xxs text-brand-slate/75 leading-relaxed bg-brand-bg p-3.5 rounded-xl border border-brand-slate/10">
            <span className="font-bold text-xxs text-brand-plum uppercase block mb-1">Healthcare Advisory:</span>
            CarePath suggestions are autonomous advisory recommendations. We provide healthcare navigation support, which does not replace qualified diagnostic procedures, medical triage, or doctors prescriptions.
          </div>
        </div>
      </div>

      {/* Prepare for appointment CTA */}
      <div className="bg-brand-lavender-light/50 border border-brand-lavender/10 p-6 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex gap-3 items-center">
          <div className="w-10 h-10 bg-brand-lavender text-white rounded-lg flex items-center justify-center shrink-0">
            <CalendarCheck className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-display font-bold text-sm text-brand-plum">Ready to consult?</h4>
            <p className="text-brand-slate text-xs">Let CarePath prepare clinical summary notes and follow-ups.</p>
          </div>
        </div>
        <Link 
          to="/journey"
          className="bg-brand-lavender hover:bg-brand-lavender-hover text-white text-xs font-semibold px-5 py-3 rounded-xl transition-all shadow-sm flex items-center gap-1.5 shrink-0"
        >
          View Care Journey Map
        </Link>
      </div>
    </div>
  );
}
