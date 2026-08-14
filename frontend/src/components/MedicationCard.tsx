import React from 'react';
import { Pill, Check, Clock, AlertTriangle, CalendarRange } from 'lucide-react';

export interface Medication {
  id: string;
  name: string;
  dose: string;
  time: string;
  frequency: string;
  instructions: string;
  status: 'taken' | 'upcoming' | 'missed';
  startDate: string;
  duration: string;
  nextDose: string;
}

interface MedicationCardProps {
  medication: Medication;
  onMarkAsTaken?: (id: string) => void;
  showDetails?: boolean;
}

export default function MedicationCard({ 
  medication, 
  onMarkAsTaken, 
  showDetails = false 
}: MedicationCardProps) {
  const getStatusStyles = () => {
    switch (medication.status) {
      case 'taken':
        return 'bg-brand-sage-bg text-brand-sage-text border-brand-sage-text/10';
      case 'missed':
        return 'bg-brand-rose-bg text-brand-rose-text border-brand-rose-text/10';
      default:
        return 'bg-brand-bg text-brand-plum border-brand-slate/15';
    }
  };

  const getStatusIcon = () => {
    switch (medication.status) {
      case 'taken':
        return <Check className="w-3 h-3" />;
      case 'missed':
        return <AlertTriangle className="w-3 h-3 text-brand-rose-text" />;
      default:
        return <Clock className="w-3 h-3" />;
    }
  };

  return (
    <div className={`bg-brand-card border border-brand-slate/10 rounded-2xl p-5 shadow-xs transition-all hover:border-brand-lavender/20 flex flex-col gap-4 ${
      medication.status === 'taken' ? 'opacity-80 bg-brand-bg/10' : ''
    }`}>
      <div className="flex items-start justify-between gap-4">
        {/* Left Section: Icon & Info */}
        <div className="flex gap-3.5 min-w-0">
          <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${
            medication.status === 'taken' 
              ? 'bg-brand-sage-bg text-brand-sage-text' 
              : medication.status === 'missed'
              ? 'bg-brand-rose-bg text-brand-rose-text'
              : 'bg-brand-lavender-light text-brand-lavender'
          }`}>
            <Pill className="w-5 h-5" />
          </div>
          <div className="min-w-0">
            <h4 className="font-display font-bold text-sm text-brand-plum truncate">{medication.name}</h4>
            <span className="text-[10px] text-brand-slate font-medium block mt-0.5">
              {medication.dose} &bull; {medication.time} &bull; {medication.frequency}
            </span>
            <p className="text-xxs text-brand-slate mt-1.5 leading-relaxed font-light">
              {medication.instructions}
            </p>
          </div>
        </div>

        {/* Right Section: Status Indicator & Log Action */}
        <div className="flex flex-col items-end gap-2 shrink-0">
          <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.75 rounded-full text-[9px] font-bold border uppercase tracking-wider ${getStatusStyles()}`}>
            {getStatusIcon()}
            <span>{medication.status}</span>
          </span>

          {medication.status === 'upcoming' && onMarkAsTaken && (
            <button
              onClick={() => onMarkAsTaken(medication.id)}
              className="text-[10px] font-bold text-white bg-brand-lavender hover:bg-brand-lavender-hover px-3 py-1.5 rounded-lg shadow-xxs transition-all cursor-pointer active:scale-98"
            >
              Mark taken
            </button>
          )}
        </div>
      </div>

      {/* Expanded Details Sub-card */}
      {showDetails && (
        <div className="border-t border-brand-slate/5 pt-3.5 grid grid-cols-2 gap-4 text-xxs text-brand-slate leading-relaxed font-light bg-brand-bg/20 p-3 rounded-xl border border-brand-slate/5">
          <div>
            <span className="font-bold text-brand-plum block mb-0.5">Treatment Timeline</span>
            <span className="flex items-center gap-1 mt-0.5">
              <CalendarRange className="w-3.5 h-3.5 text-brand-slate/60 shrink-0" />
              Started {medication.startDate} &bull; {medication.duration}
            </span>
          </div>
          <div>
            <span className="font-bold text-brand-plum block mb-0.5">Next Scheduled Dose</span>
            <span className="flex items-center gap-1 mt-0.5">
              <Clock className="w-3.5 h-3.5 text-brand-slate/60 shrink-0" />
              {medication.nextDose}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
