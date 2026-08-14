import React, { useEffect, useState } from 'react';
import { usePatient } from '../context/PatientContext';
import { timelineService } from '../services/timelineService';
import { 
  Activity, 
  FileText, 
  Sparkles, 
  Pill, 
  Stethoscope, 
  UserCheck, 
  Calendar, 
  CheckSquare, 
  Clock, 
  PlusCircle, 
  X, 
  ArrowUpRight,
  FileSpreadsheet,
  AlertCircle,
  HelpCircle,
  TrendingUp,
  Inbox
} from 'lucide-react';
import { Link } from 'react-router-dom';
import type { TimelineEvent, TimelineEventType } from '../types';

export default function TimelinePage() {
  const { patient } = usePatient();
  const [events, setEvents] = useState<TimelineEvent[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [activeFilter, setActiveFilter] = useState<string>('All');
  const [selectedEvent, setSelectedEvent] = useState<TimelineEvent | null>(null);

  // New event modal
  const [modalOpen, setModalOpen] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [newType, setNewType] = useState<TimelineEventType>('symptom');
  const [newDetails, setNewDetails] = useState('');
  const [newSource, setNewSource] = useState('Patient Logged');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchTimeline = async () => {
    if (!patient) return;
    setIsLoading(true);
    setError(null);
    try {
      const data = await timelineService.getTimeline(patient.id);
      const sorted = [...data].sort((a, b) => 
        new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
      );
      setEvents(sorted);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Failed to fetch journey timeline events. Verify local API.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTimeline();
    window.addEventListener('timeline_updated', fetchTimeline);
    return () => {
      window.removeEventListener('timeline_updated', fetchTimeline);
    };
  }, [patient]);

  const handleAddEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!patient || !newTitle || !newDesc) return;
    setIsSubmitting(true);

    const eventPayload = {
      patient_id: patient.id,
      type: newType,
      title: newTitle,
      description: newDesc,
      details: newDetails,
      timestamp: new Date().toISOString()
    };

    try {
      if (patient.id === 'demo_patient_id') {
        const mockNewEvent: TimelineEvent = {
          id: `ev_custom_${Date.now()}`,
          ...eventPayload
        };
        setEvents(prev => [mockNewEvent, ...prev]);
      } else {
        await timelineService.addTimelineEvent(eventPayload);
        await fetchTimeline();
      }
      setModalOpen(false);
      setNewTitle('');
      setNewDesc('');
      setNewDetails('');
      setNewSource('Patient Logged');
    } catch (err: any) {
      console.error(err);
      alert(err.message || 'Failed to append event to timeline.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getEventMeta = (type: TimelineEventType) => {
    switch (type) {
      case 'symptom':
        return { icon: Activity, bg: 'bg-brand-amber-bg text-brand-amber-text border-brand-amber-text/10', label: 'Symptom', link: '/followup' };
      case 'document':
        return { icon: FileText, bg: 'bg-brand-lavender-light text-brand-lavender border-brand-lavender/10', label: 'Document', link: '/records' };
      case 'test':
        return { icon: FileSpreadsheet, bg: 'bg-brand-bg text-brand-plum border-brand-slate/15', label: 'Diagnostics', link: '/records' };
      case 'medication':
        return { icon: Pill, bg: 'bg-brand-lavender-light text-brand-lavender border-brand-lavender/10', label: 'Medication', link: '/medications' };
      case 'doctor':
        return { icon: Stethoscope, bg: 'bg-brand-sage-bg text-brand-sage-text border-brand-sage-text/10', label: 'Doctor Bridge', link: '/doctor-bridge' };
      case 'referral':
        return { icon: UserCheck, bg: 'bg-brand-sage-bg text-brand-sage-text border-brand-sage-text/10', label: 'Referral Route', link: '/journey' };
      case 'analysis':
        return { icon: Sparkles, bg: 'bg-brand-lavender text-white border-brand-lavender/10', label: 'AI Insight', link: '/analysis' };
      case 'followup':
        return { icon: Calendar, bg: 'bg-brand-sage-bg text-brand-sage-text border-brand-sage-text/10', label: 'Follow-up', link: '/followup' };
      case 'careplan':
        return { icon: CheckSquare, bg: 'bg-brand-bg text-brand-slate border-brand-slate/10', label: 'Care Plan', link: '/analysis' };
      default:
        return { icon: HelpCircle, bg: 'bg-brand-bg text-brand-slate border-brand-slate/10', label: 'Event', link: '/dashboard' };
    }
  };

  const getFilteredEvents = () => {
    if (activeFilter === 'All') return events;
    return events.filter(e => {
      const meta = getEventMeta(e.type);
      return meta.label.toLowerCase().includes(activeFilter.toLowerCase()) || 
             e.type.toLowerCase().includes(activeFilter.toLowerCase());
    });
  };

  const filteredEvents = getFilteredEvents();

  return (
    <div className="flex flex-col gap-8">
      {/* Header */}
      <div className="flex items-center justify-between gap-4 flex-wrap border-b border-brand-slate/10 pb-4">
        <div>
          <h1 className="font-display text-2xl md:text-3xl font-bold tracking-tight text-brand-plum mb-1">
            My Care Timeline
          </h1>
          <p className="text-brand-slate text-xs font-light">
            Your continuous chronological healthcare mapping history and actions.
          </p>
        </div>
        <button
          onClick={() => setModalOpen(true)}
          className="flex items-center justify-center gap-1.5 bg-brand-lavender hover:bg-brand-lavender-hover text-white text-xs font-semibold px-4 py-2.5 rounded-xl transition-all shadow-sm cursor-pointer"
        >
          <PlusCircle className="w-4 h-4" />
          Add Timeline Event
        </button>
      </div>

      {error && (
        <div className="bg-brand-rose-bg border border-brand-rose-text/10 text-brand-rose-text p-4 rounded-xl text-sm flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <AlertCircle className="w-5 h-5 shrink-0" />
            <span>{error}</span>
          </div>
          <button onClick={fetchTimeline} className="text-xs font-bold underline">Retry</button>
        </div>
      )}

      {/* Filter Chips Bar */}
      <div className="flex flex-wrap gap-2.5 pb-2">
        {[
          'All',
          'Symptoms',
          'Tests',
          'Documents',
          'Medication',
          'Doctor',
          'AI Insights',
          'Follow-up'
        ].map(filter => (
          <button
            key={filter}
            onClick={() => setActiveFilter(filter)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-all cursor-pointer ${
              activeFilter === filter
                ? 'bg-brand-plum text-white border-brand-plum shadow-xxs'
                : 'bg-brand-card border-brand-slate/10 text-brand-slate hover:border-brand-slate/20 hover:bg-brand-bg/50'
            }`}
          >
            {filter}
          </button>
        ))}
      </div>

      {/* Grid: Timeline Flow on Left, Selected Event Details on Right */}
      {isLoading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-brand-lavender mb-4"></div>
          <p className="text-brand-slate text-sm font-light">Loading timeline logs...</p>
        </div>
      ) : filteredEvents.length === 0 ? (
        <div className="bg-brand-card border border-brand-slate/10 p-12 rounded-3xl text-center flex flex-col items-center gap-6 my-6 max-w-xl mx-auto shadow-xxs">
          <div className="w-14 h-14 bg-brand-bg rounded-full flex items-center justify-center text-brand-slate">
            <Inbox className="w-6 h-6" />
          </div>
          <div>
            <h2 className="font-display text-base font-bold text-brand-plum mb-2">No matching timeline milestones</h2>
            <p className="text-brand-slate text-xs max-w-xs leading-relaxed mx-auto font-light">
              Clear your active filters or log a custom event to preview milestone trackers.
            </p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">
          {/* Left: Interactive Vertical Thread Timeline (3 Cols) */}
          <div className="lg:col-span-3 flex flex-col relative border-l border-brand-slate/15 ml-4 pl-6 md:pl-8 py-2 gap-6">
            {filteredEvents.map((event) => {
              const meta = getEventMeta(event.type);
              const Icon = meta.icon;
              const isSelected = selectedEvent?.id === event.id;

              return (
                <div 
                  key={event.id} 
                  onClick={() => setSelectedEvent(event)}
                  className="relative group cursor-pointer"
                >
                  {/* Timeline circle node */}
                  <div className={`absolute -left-10.5 md:-left-12.5 top-1.5 w-9 h-9 rounded-full border flex items-center justify-center shadow-xxs transition-all ${meta.bg} ${
                    isSelected ? 'ring-2 ring-brand-plum border-brand-plum scale-110' : 'group-hover:scale-105'
                  }`}>
                    <Icon className="w-4 h-4" />
                  </div>

                  {/* Event Card */}
                  <div className={`border rounded-2xl p-4 md:p-5 shadow-xxs transition-all flex flex-col gap-2 ${
                    isSelected 
                      ? 'border-brand-lavender bg-brand-lavender-light/10 ring-1 ring-brand-lavender/10' 
                      : 'border-brand-slate/10 bg-brand-card hover:border-brand-slate/20 hover:shadow-xs'
                  }`}>
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-brand-slate/5 pb-2">
                      <span className={`text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded border max-w-fit ${meta.bg}`}>
                        {meta.label}
                      </span>
                      
                      <span className="text-[10px] text-brand-slate/60 font-light flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5" />
                        {new Date(event.timestamp).toLocaleDateString(undefined, { 
                          month: 'short', 
                          day: 'numeric',
                          year: 'numeric'
                        })}
                      </span>
                    </div>

                    <h3 className="font-display font-bold text-sm text-brand-plum mt-1">{event.title}</h3>
                    <p className="text-brand-slate text-xs leading-relaxed font-light">
                      {event.description}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Right: Selected Event Details Panel (2 Cols) */}
          <div className="lg:col-span-2 lg:sticky lg:top-4 flex flex-col gap-6">
            {selectedEvent ? (
              <div className="bg-brand-card border border-brand-slate/10 p-6 rounded-3xl shadow-sm flex flex-col gap-5 animate-in fade-in duration-300">
                <div className="flex justify-between items-start border-b border-brand-slate/10 pb-4">
                  <div>
                    <span className="text-[9px] font-bold text-brand-slate uppercase tracking-wider">Inspected Milestone</span>
                    <h3 className="font-display font-extrabold text-sm text-brand-plum mt-1">{selectedEvent.title}</h3>
                  </div>
                  <button 
                    onClick={() => setSelectedEvent(null)}
                    className="p-1 rounded-lg hover:bg-brand-bg text-brand-slate hover:text-brand-plum transition-all"
                  >
                    <X className="w-4.5 h-4.5" />
                  </button>
                </div>

                <div className="flex flex-col gap-4 text-xxs leading-relaxed font-light text-brand-slate">
                  <div>
                    <span className="font-bold text-brand-plum block">Log Category Type</span>
                    <span className="text-xs">{getEventMeta(selectedEvent.type).label}</span>
                  </div>
                  <div>
                    <span className="font-bold text-brand-plum block">Timestamp</span>
                    <span>
                      {new Date(selectedEvent.timestamp).toLocaleDateString(undefined, { 
                        weekday: 'long',
                        month: 'long', 
                        day: 'numeric',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  </div>

                  <div>
                    <span className="font-bold text-brand-plum block">Milestone Description</span>
                    <span className="text-brand-plum block mt-0.5">{selectedEvent.description}</span>
                  </div>

                  {selectedEvent.details && (
                    <div className="bg-brand-bg/50 border border-brand-slate/10 p-4 rounded-xl">
                      <span className="font-bold text-brand-plum block mb-1">Clinical Notes & Findings</span>
                      <p className="text-brand-plum italic leading-relaxed">
                        "{selectedEvent.details}"
                      </p>
                    </div>
                  )}
                </div>

                {/* Unified Related Feature Redirect Button */}
                <div className="border-t border-brand-slate/10 pt-4 mt-2">
                  <Link
                    to={getEventMeta(selectedEvent.type).link}
                    className="bg-brand-lavender hover:bg-brand-lavender-hover text-white text-xs font-semibold px-5 py-3 rounded-xl transition-all shadow-sm flex items-center justify-center gap-1.5 cursor-pointer"
                  >
                    Go to Related Section
                    <ArrowUpRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            ) : (
              <div className="bg-brand-card border border-brand-slate/10 p-8 rounded-3xl text-center flex flex-col items-center gap-4 py-16 shadow-xxs">
                <div className="w-12 h-12 bg-brand-bg rounded-2xl flex items-center justify-center text-brand-slate/40">
                  <TrendingUp className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="font-display font-bold text-xs text-brand-plum">Milestone Deep-dive</h4>
                  <p className="text-[11px] text-brand-slate font-light max-w-xs mt-1.5">
                    Click any timeline event card on the left to inspect detailed clinical annotations and follow associated routing links.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Add Event Modal Overlay */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-brand-plum/45 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-brand-card w-full max-w-md rounded-3xl border border-brand-slate/10 p-6 shadow-md flex flex-col gap-4 animate-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between border-b border-brand-slate/10 pb-3">
              <h3 className="font-display font-bold text-sm text-brand-plum">Log Timeline Milestone</h3>
              <button 
                onClick={() => setModalOpen(false)}
                className="p-1 rounded-lg hover:bg-brand-bg text-brand-slate"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleAddEvent} className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-[10px] font-bold text-brand-slate uppercase tracking-wider">Event Title</label>
                <input 
                  type="text" 
                  placeholder="e.g. Consulted General Practitioner"
                  value={newTitle} 
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-4 py-2.5 text-xs text-brand-plum outline-none focus:border-brand-lavender transition-all"
                  required
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-[10px] font-bold text-brand-slate uppercase tracking-wider">Event Category</label>
                <select 
                  value={newType} 
                  onChange={(e) => setNewType(e.target.value as TimelineEventType)}
                  className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-4 py-2.5 text-xs text-brand-plum cursor-pointer outline-none focus:border-brand-lavender transition-all font-medium"
                >
                  <option value="symptom">Symptom Logging</option>
                  <option value="document">Document Upload</option>
                  <option value="test">Diagnostics & Tests</option>
                  <option value="medication">Medication Log</option>
                  <option value="doctor">Doctor Consultation</option>
                  <option value="referral">Referral Update</option>
                  <option value="analysis">AI Insight</option>
                  <option value="followup">Follow-up check-in</option>
                  <option value="careplan">Care Plan Goal</option>
                </select>
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-[10px] font-bold text-brand-slate uppercase tracking-wider">Short Summary</label>
                <input 
                  type="text" 
                  placeholder="Brief summary of the milestone"
                  value={newDesc} 
                  onChange={(e) => setNewDesc(e.target.value)}
                  className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-4 py-2.5 text-xs text-brand-plum outline-none focus:border-brand-lavender transition-all"
                  required
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-[10px] font-bold text-brand-slate uppercase tracking-wider">Clinical Details (Optional)</label>
                <textarea 
                  rows={3}
                  placeholder="Extra advice, symptoms changes, or diagnosis notes..."
                  value={newDetails} 
                  onChange={(e) => setNewDetails(e.target.value)}
                  className="w-full bg-brand-bg border border-brand-slate/15 rounded-xl px-4 py-2.5 text-xs text-brand-plum outline-none focus:border-brand-lavender transition-all resize-none leading-relaxed"
                />
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="bg-brand-lavender hover:bg-brand-lavender-hover text-white text-xs font-semibold py-3 rounded-xl transition-all shadow-sm flex items-center justify-center gap-1.5 cursor-pointer mt-2"
              >
                Log Event
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
