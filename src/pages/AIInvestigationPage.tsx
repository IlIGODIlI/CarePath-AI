import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { analysisService } from '../services/analysisService';
import { 
  Sparkles, 
  CheckCircle, 
  Clock, 
  AlertCircle, 
  Loader2, 
  HelpCircle,
  Activity
} from 'lucide-react';
import type { AgentName, AgentState } from '../types';

export default function AIInvestigationPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const analysisId = searchParams.get('id');
  const isDemo = searchParams.get('demo') === 'true';


  const [agentStates, setAgentStates] = useState<Record<AgentName, AgentState> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [dots, setDots] = useState('');

  // Agent names list in typical sequence
  const pipeline: AgentName[] = [
    'Supervisor',
    'Intake',
    'Vision',
    'Docs',
    'Timeline',
    'Evidence',
    'Clinical Reasoning',
    'Safety',
    'Referral',
    'Care Plan',
    'Follow-up'
  ];

  // Typing dots animation
  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? '' : prev + '.'));
    }, 600);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (isDemo) {
      // Simulate progress for hackathon demo
      const demoStates: Record<AgentName, AgentState> = pipeline.reduce((acc, name) => {
        acc[name] = { status: 'idle' };
        return acc;
      }, {} as Record<AgentName, AgentState>);
      setAgentStates(demoStates);

      let step = 0;
      const demoTimer = setInterval(() => {
        setAgentStates((prev) => {
          if (!prev) return null;
          const next = { ...prev };
          const activeAgent = pipeline[step];
          
          // Complete previous
          if (step > 0) {
            next[pipeline[step - 1]] = { status: 'completed', message: 'Task finalized.' };
          }
          // Set current running
          if (activeAgent) {
            next[activeAgent] = { status: 'running', message: `Analyzing medical context${dots}` };
          }
          return next;
        });

        step++;
        if (step > pipeline.length) {
          clearInterval(demoTimer);
          navigate('/analysis');
        }
      }, 1000);

      return () => clearInterval(demoTimer);
    }

    if (!analysisId) {
      setError('Missing Analysis ID parameter.');
      return;
    }

    // Polling real backend
    const pollInterval = setInterval(async () => {
      try {
        const result = await analysisService.getAnalysis(analysisId);

        if (result.agent_states) {
          setAgentStates(result.agent_states as Record<AgentName, AgentState>);
        }
        
        if (result.status === 'completed') {
          clearInterval(pollInterval);
          navigate('/analysis');
        } else if (result.status === 'failed') {
          clearInterval(pollInterval);
          setError('The clinical mapping process encountered an unexpected failure.');
        }
      } catch (err: any) {
        console.error('Error polling analysis:', err);
        // Do not immediately fail on network hiccup, let polling retry
      }
    }, 2000);

    return () => clearInterval(pollInterval);
  }, [analysisId, isDemo, navigate]);

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-8">
      {/* Header section */}
      <div className="text-center py-6 flex flex-col items-center">
        <div className="w-14 h-14 rounded-2xl bg-brand-lavender-light text-brand-lavender flex items-center justify-center mb-6 animate-pulse">
          <Sparkles className="w-7 h-7 fill-current" />
        </div>
        <h1 className="font-display text-3xl font-bold text-brand-plum mb-3">
          CarePath is mapping your journey
        </h1>
        <p className="text-brand-slate text-sm max-w-md leading-relaxed font-light">
          Our specialized clinical reasoning agents are reading your history, extracting report findings, and preparing specialist recommendations.
        </p>
      </div>

      {error && (
        <div className="bg-brand-rose-bg border border-brand-rose-text/10 text-brand-rose-text p-4 rounded-xl text-sm flex items-center gap-2.5">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Agents workflow list */}
      <div className="bg-brand-card border border-brand-slate/10 p-6 md:p-8 rounded-2xl shadow-sm">
        <h3 className="font-display text-sm font-bold tracking-wider text-brand-slate uppercase mb-6 flex items-center gap-2">
          <Activity className="w-4 h-4 text-brand-lavender" />
          Clinical Pipeline Workflow
        </h3>

        {agentStates ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {pipeline.map((agentName) => {
              const state = agentStates[agentName] || { status: 'idle' };
              let statusColor = 'bg-brand-bg text-brand-slate/60 border-brand-slate/10';
              let Icon = HelpCircle;

              if (state.status === 'running') {
                statusColor = 'bg-brand-lavender-light text-brand-lavender border-brand-lavender/30 ring-2 ring-brand-lavender/10';
                Icon = Loader2;
              } else if (state.status === 'completed') {
                statusColor = 'bg-brand-sage-bg text-brand-sage-text border-brand-sage-text/10';
                Icon = CheckCircle;
              } else if (state.status === 'failed') {
                statusColor = 'bg-brand-rose-bg text-brand-rose-text border-brand-rose-text/15';
                Icon = AlertCircle;
              } else {
                Icon = Clock;
              }

              return (
                <div 
                  key={agentName}
                  className={`border p-4 rounded-xl flex items-center gap-3 transition-all ${statusColor}`}
                >
                  <Icon className={`w-4 h-4 shrink-0 ${state.status === 'running' ? 'animate-spin' : ''}`} />
                  <div>
                    <h4 className="text-xs font-semibold">{agentName} Agent</h4>
                    <p className="text-xxxxs opacity-80 mt-0.5 max-w-[150px] truncate">
                      {state.message || (state.status === 'idle' ? 'Pending activation' : 'Workflow in queue')}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-12">
            <Loader2 className="w-8 h-8 text-brand-lavender animate-spin mb-3" />
            <p className="text-xs text-brand-slate">Contacting Clinical Supervisors{dots}</p>
          </div>
        )}
      </div>
    </div>
  );
}
