import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { usePatient } from '../context/PatientContext';
import { useAuth } from '../context/AuthContext';
import { timelineService } from '../services/timelineService';
import { analysisService } from '../services/analysisService';
import { 
  Compass, 
  ArrowRight, 
  Activity, 
  Eye, 
  Users2, 
  Calendar, 
  RefreshCw, 
  AlertCircle, 
  CheckCircle2,
  Clock
} from 'lucide-react';
import type { TimelineEvent, AnalysisResult } from '../types';

export default function DashBoardingPage() {
  const { patient, isLoading: isPatientLoading, error: patientError, fetchPatient } = usePatient();
  const { user } = useAuth();
  
  const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
  const [latestAnalysis, setLatestAnalysis] = useState<AnalysisResult | null>(null);
  const [isLoadingData, setIsLoadingData] = useState(false);
  const [isOffline, setIsOffline] = useState(false);

  useEffect(() => {
    const loadDashboardData = async () => {
      if (!patient) return;
      setIsLoadingData(true);
      setIsOffline(false);
      try {
        if (patient.id === 'demo_patient_id') {
          // Mock data for demo
          setTimeline([
            {
              id: '1',
              patient_id: 'demo_patient_id',
              type: 'symptom',
              title: 'Symptoms Logged',
              description: 'Initial log of cough and mild shortness of breath.',
              timestamp: new Date(Date.now() - 86400000 * 2).toISOString(),
            },
            {
              id: '2',
              patient_id: 'demo_patient_id',
              type: 'upload',
              title: 'Uploaded Lab Report',
              description: 'Chest X-ray report and CBC blood test results.',
              timestamp: new Date(Date.now() - 86400000).toISOString(),
            }
          ]);
          setLatestAnalysis({
            id: 'demo_analysis',
            patient_id: 'demo_patient_id',
            status: 'completed',
            specialist_recommendation: 'Pulmonologist / Respirologist',
            explanation: 'Based on your persistent cough and mild shortness of breath alongside chest X-ray findings, a consultation with a pulmonologist is recommended to assess respiratory function.',
            considered_factors: ['Dry cough lasting 3 days', 'Chest X-ray report uploaded', 'Mild exertion-induced shortness of breath'],
            safety_alerts: ['If chest pain, severe shortness of breath, or high fever develops, seek emergency care immediately.'],
            created_at: new Date(Date.now() - 3600000 * 2).toISOString(),
          });
        } else {
          // Real backend fetch
          const [events, history] = await Promise.all([
            timelineService.getTimeline(patient.id),
            analysisService.getAnalysisHistory(patient.id),
          ]);
          setTimeline(events);
          if (history && history.length > 0) {
            // Sort by created_at descending
            const sorted = [...history].sort((a, b) => 
              new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
            );
            setLatestAnalysis(sorted[0]);
          }
        }
      } catch (err: any) {
        console.error('Error fetching dashboard data:', err);
        setIsOffline(true);
      } finally {
        setIsLoadingData(false);
      }
    };

    loadDashboardData();
  }, [patient]);

  // Determine active stage on the map
  const getActiveStage = () => {
    if (!latestAnalysis) return 1; // Symptoms logged
    if (latestAnalysis.status === 'processing') return 2; // Analysis running
    if (latestAnalysis.specialist_recommendation) return 3; // Specialist recommended
    if (timeline.some(e => e.type === 'consultation')) return 4; // Consultation
    if (timeline.some(e => e.type === 'followup')) return 5; // Follow-up
    return 3;
  };

  const currentStage = getActiveStage();

  const stages = [
    { number: 1, name: 'Symptoms', icon: Activity, desc: 'Logged symptoms & profile' },
    { number: 2, name: 'Understanding', icon: Eye, desc: 'AI parsing & documents' },
    { number: 3, name: 'Specialist', icon: Users2, desc: 'Specialist recommendation' },
    { number: 4, name: 'Consultation', icon: Calendar, desc: 'Doctor appointment' },
    { number: 5, name: 'Follow-up', icon: RefreshCw, desc: 'Recovery tracker' }
  ];

  if (isPatientLoading || isLoadingData) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-brand-lavender mb-4"></div>
        <p className="text-brand-slate text-sm">Synchronizing your care map...</p>
      </div>
    );
  }

  if (patientError) {
    return (
      <div className="bg-brand-rose-bg border border-brand-rose-text/10 text-brand-rose-text p-6 rounded-2xl flex flex-col gap-4 max-w-2xl mx-auto my-10">
        <div className="flex items-center gap-3">
          <AlertCircle className="w-6 h-6 shrink-0" />
          <h3 className="font-display font-semibold text-lg">Unable to load patient records</h3>
        </div>
        <p className="text-sm">{patientError}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="bg-brand-rose-text text-white text-xs font-semibold px-4 py-2 rounded-xl w-fit"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-8">
      {/* Offline Alert Banner */}
      {isOffline && (
        <div className="bg-brand-amber-bg border border-brand-amber-text/10 text-brand-amber-text p-4 rounded-2xl flex items-center justify-between text-sm">
          <div className="flex items-center gap-2.5">
            <AlertCircle className="w-5 h-5" />
            <span>CarePath cannot contact the local API server. Showing demo data for visualization.</span>
          </div>
          <button 
            onClick={() => patient && fetchPatient(patient.id)}
            className="text-xs font-semibold underline hover:no-underline"
          >
            Retry Connection
          </button>
        </div>
      )}

      {/* Hero Welcome */}
      <div>
        <h1 className="font-display text-3xl font-bold tracking-tight text-brand-plum mb-1">
          Welcome back, {patient?.name || user?.name || 'Patient'}
        </h1>
        <p className="text-brand-slate text-sm">
          Here is the current state of your autonomous healthcare journey.
        </p>
      </div>

      {/* Journey Map Row */}
      <div className="bg-brand-card border border-brand-slate/10 p-6 md:p-8 rounded-2xl shadow-sm">
        <h2 className="font-display text-lg font-semibold mb-6 flex items-center gap-2">
          <Compass className="w-5 h-5 text-brand-lavender" />
          CarePath Map
        </h2>

        {/* Map Timeline Grid */}
        <div className="relative flex flex-col md:flex-row justify-between gap-6 md:gap-4">
          {/* Connector Line Desktop */}
          <div className="hidden md:block absolute top-6 left-6 right-6 h-0.5 bg-brand-slate/10 -z-10" />

          {stages.map((stage) => {
            const Icon = stage.icon;
            const isCompleted = stage.number < currentStage;
            const isCurrent = stage.number === currentStage;
            
            return (
              <div 
                key={stage.number} 
                className={`flex flex-row md:flex-col items-center gap-4 md:text-center flex-1 transition-all ${
                  isCurrent ? 'scale-102' : ''
                }`}
              >
                {/* Stage Circle */}
                <div 
                  className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-all ${
                    isCompleted 
                      ? 'bg-brand-sage-bg border-brand-sage-text text-brand-sage-text shadow-sm'
                      : isCurrent
                      ? 'bg-brand-lavender-light border-brand-lavender text-brand-lavender font-bold scale-110 shadow-md ring-4 ring-brand-lavender/10'
                      : 'bg-brand-card border-brand-slate/20 text-brand-slate'
                  }`}
                >
                  {isCompleted ? (
                    <CheckCircle2 className="w-5 h-5 stroke-[2.5]" />
                  ) : (
                    <Icon className="w-5 h-5" />
                  )}
                </div>

                <div className="flex flex-col md:items-center">
                  <span className={`text-sm font-semibold ${
                    isCurrent ? 'text-brand-plum font-bold' : isCompleted ? 'text-brand-slate' : 'text-brand-slate/60'
                  }`}>
                    {stage.name}
                  </span>
                  <span className="text-xxs text-brand-slate/75 hidden md:block max-w-xs mt-1">
                    {stage.desc}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Next Step & Explanation Panels */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Next Step Panel */}
        <div className="bg-brand-card border border-brand-slate/10 p-6 rounded-2xl shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <span className="text-xxs font-bold tracking-wider text-brand-lavender uppercase bg-brand-lavender-light px-2.5 py-1 rounded-full">
                Active Step
              </span>
            </div>
            
            <h3 className="font-display text-xl font-bold text-brand-plum mb-3">
              {latestAnalysis?.specialist_recommendation 
                ? `Consult a ${latestAnalysis.specialist_recommendation}`
                : 'Upload Medical Materials to Start Analysis'}
            </h3>

            <p className="text-brand-slate text-sm leading-relaxed mb-6 font-light">
              {latestAnalysis?.specialist_recommendation
                ? latestAnalysis.explanation
                : 'Provide symptom description, lab results, prescriptions, or imaging reports. Our multi-agent clinical reasoning engine will structure a recovery timeline and match you with the appropriate specialist.'}
            </p>
          </div>

          <div className="flex items-center gap-4">
            {latestAnalysis?.specialist_recommendation ? (
              <Link 
                to="/analysis"
                className="flex items-center gap-1.5 text-sm font-bold text-brand-lavender hover:text-brand-lavender-hover transition-colors"
              >
                Review Analysis Results
                <ArrowRight className="w-4 h-4" />
              </Link>
            ) : (
              <Link 
                to="/upload"
                className="flex items-center gap-2 bg-brand-lavender hover:bg-brand-lavender-hover text-white text-xs font-semibold px-5 py-3 rounded-xl transition-all shadow-sm"
              >
                Upload Medical Documents
                <ArrowRight className="w-4 h-4" />
              </Link>
            )}
          </div>
        </div>

        {/* Why This Matters Panel */}
        <div className="bg-brand-card border border-brand-slate/10 p-6 rounded-2xl shadow-sm">
          <h3 className="font-display text-sm font-bold tracking-wider text-brand-slate uppercase mb-4">
            Why This Matters
          </h3>
          
          {latestAnalysis?.considered_factors && latestAnalysis.considered_factors.length > 0 ? (
            <div className="flex flex-col gap-3">
              <p className="text-xs text-brand-slate leading-relaxed">
                CarePath reached this guidance by analyzing clinical relationships in your uploaded documents and logged history:
              </p>
              <ul className="flex flex-col gap-2">
                {latestAnalysis.considered_factors.map((factor, idx) => (
                  <li key={idx} className="flex gap-2.5 items-start text-xs text-brand-plum">
                    <span className="w-4.5 h-4.5 rounded-full bg-brand-lavender-light text-brand-lavender font-bold flex items-center justify-center shrink-0 text-xxs">
                      {idx + 1}
                    </span>
                    <span>{factor}</span>
                  </li>
                ))}
              </ul>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Compass className="w-8 h-8 text-brand-slate/40 mb-3" />
              <p className="text-xs text-brand-slate leading-relaxed max-w-xs">
                Once documents are analyzed, CarePath lists the critical factors and clinical rationale here.
              </p>
            </div>
          )}

          {/* Safety Warning */}
          {latestAnalysis?.safety_alerts && latestAnalysis.safety_alerts.length > 0 && (
            <div className="mt-5 p-3 rounded-xl bg-brand-rose-bg/75 border border-brand-rose-text/10 text-brand-rose-text text-xxs flex gap-2">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold">Safety Note: </span>
                {latestAnalysis.safety_alerts[0]}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Recent Activity and Records */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="bg-brand-card border border-brand-slate/10 p-6 rounded-2xl shadow-sm">
          <h3 className="font-display text-md font-semibold text-brand-plum mb-4">Recent Activity</h3>
          
          {timeline.length > 0 ? (
            <div className="flex flex-col gap-4">
              {timeline.slice(0, 3).map((event) => (
                <div key={event.id} className="flex gap-3 items-start border-b border-brand-slate/5 pb-3 last:border-0 last:pb-0">
                  <div className="w-8 h-8 rounded-lg bg-brand-bg flex items-center justify-center text-brand-slate shrink-0">
                    <Clock className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-xs font-semibold text-brand-plum">{event.title}</h4>
                    <p className="text-xxs text-brand-slate mt-0.5">{event.description}</p>
                    <span className="text-xxxxs text-brand-slate/60 block mt-1">
                      {new Date(event.timestamp).toLocaleDateString(undefined, { 
                        month: 'short', 
                        day: 'numeric', 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </span>
                  </div>
                </div>
              ))}
              <Link 
                to="/journey" 
                className="text-xxs font-semibold text-brand-lavender hover:underline w-fit mt-2"
              >
                View Full Timeline
              </Link>
            </div>
          ) : (
            <div className="py-8 text-center">
              <p className="text-xs text-brand-slate">No recent activity logged.</p>
            </div>
          )}
        </div>

        {/* Your Records Summary */}
        <div className="bg-brand-card border border-brand-slate/10 p-6 rounded-2xl shadow-sm">
          <h3 className="font-display text-md font-semibold text-brand-plum mb-4">Medical Documents</h3>
          
          {patient?.current_symptoms ? (
            <div className="flex flex-col gap-4 justify-between h-[calc(100%-2rem)]">
              <div className="bg-brand-bg p-4 rounded-xl border border-brand-slate/10">
                <h4 className="text-xxs font-bold tracking-wider text-brand-slate uppercase mb-1.5">Logged Symptoms</h4>
                <p className="text-xs text-brand-plum leading-relaxed italic font-light">
                  "{patient.current_symptoms}"
                </p>
              </div>
              <div className="flex items-center justify-between border-t border-brand-slate/10 pt-4 mt-2">
                <span className="text-xxs text-brand-slate">
                  Age: {patient.age} | Gender: {patient.gender}
                </span>
                <Link 
                  to="/records"
                  className="text-xxs font-semibold text-brand-lavender hover:underline"
                >
                  Manage Records
                </Link>
              </div>
            </div>
          ) : (
            <div className="py-8 text-center flex flex-col items-center justify-center">
              <p className="text-xs text-brand-slate mb-4">No records or symptoms uploaded yet.</p>
              <Link 
                to="/profile" 
                className="bg-brand-lavender hover:bg-brand-lavender-hover text-white text-xxs font-semibold px-4 py-2.5 rounded-lg transition-all shadow-sm"
              >
                Setup Patient Context
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
