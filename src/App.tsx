import React, { useState } from 'react';
import { TabType } from './types';
import { Header } from './components/Header';
import { ArchitectureBlueprintView } from './components/Tabs/ArchitectureBlueprintView';
import { FolderStructureExplorer } from './components/Tabs/FolderStructureExplorer';
import { LangGraphAgentSimulator } from './components/Tabs/LangGraphAgentSimulator';
import { ApiContractExplorer } from './components/Tabs/ApiContractExplorer';
import { DatabaseSchemaViewer } from './components/Tabs/DatabaseSchemaViewer';
import { SecurityPhiSandbox } from './components/Tabs/SecurityPhiSandbox';

export default function App() {
  const [activeTab, setActiveTab] = useState<TabType>('blueprint');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans antialiased flex flex-col">
      {/* Fixed Sticky Header */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main View Area */}
      <main className="flex-1 pb-12">
        {activeTab === 'blueprint' && <ArchitectureBlueprintView />}
        {activeTab === 'folder-structure' && <FolderStructureExplorer />}
        {activeTab === 'langgraph-visualizer' && <LangGraphAgentSimulator />}
        {activeTab === 'api-contracts' && <ApiContractExplorer />}
        {activeTab === 'database-schema' && <DatabaseSchemaViewer />}
        {activeTab === 'security-phi' && <SecurityPhiSandbox />}
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 border-t border-slate-800/80 py-4 text-xs text-slate-500 text-center">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>
            CarePath AI &bull; Autonomous Healthcare Navigation Platform &bull; Sprint 0 Architecture Blueprint
          </span>
          <span className="font-mono text-slate-400">
            FastAPI + LangGraph Multi-Agent Stack
          </span>
        </div>
      </footer>
    </div>
  );
}
