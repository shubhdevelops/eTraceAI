'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { UploadCloud, FileText, Activity, Database, CheckCircle, ChevronRight, Dna, Info, Download } from 'lucide-react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';

export default function Home() {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<string | null>(null);
  const [jobResult, setJobResult] = useState<any>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setJobId(null);
    setJobStatus(null);
    setJobResult(null);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${baseUrl}/api/v1/upload/`, {
        method: 'POST',
        body: formData,
      });
      
      const data = await res.json();
      if (res.ok) {
        setJobId(data.job_id);
        setJobStatus('PENDING');
      } else {
        alert(`Error: ${data.detail || 'Upload failed'}`);
      }
    } catch (err) {
      alert('Failed to connect to backend. Is it running on port 8000?');
      console.error(err);
    } finally {
      setIsUploading(false);
    }
  };

  useEffect(() => {
    if (!jobId || jobStatus === 'SUCCESS' || jobStatus === 'FAILURE') return;

    const interval = setInterval(async () => {
      try {
        const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const res = await fetch(`${baseUrl}/api/v1/jobs/${jobId}`);
        const data = await res.json();
        
        setJobStatus(data.status);
        if (data.status === 'SUCCESS') {
          setJobResult(data.result);
          clearInterval(interval);
        } else if (data.status === 'FAILURE') {
          setJobResult({ error: data.error || "Job failed internally." });
          clearInterval(interval);
        }
      } catch (e) {
        console.error("Polling error", e);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId, jobStatus]);

  const handleDownloadCSV = () => {
    if (!jobResult || !jobResult.sequences) return;
    const header = "Sequence ID,Organism Match,Marine Score,Novelty Score,Classification\n";
    const rows = jobResult.sequences.map((s: any) => 
      `${s.id},${s.organism},${s.dl_marine_score},${s.novelty_score},${s.status}`
    ).join("\n");
    const blob = new Blob([header + rows], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `etrace_results_${jobId}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const MetricCard = ({ title, value, colorClass, subtitle }: { title: string, value: any, colorClass: string, subtitle?: string }) => (
    <div className="glass-card p-6 rounded-xl border border-white/5 flex flex-col justify-center items-center text-center">
      <p className="text-xs text-zinc-400 mb-2 uppercase tracking-widest font-semibold">{title}</p>
      <p className={`text-4xl font-bold ${colorClass}`}>{value}</p>
      {subtitle && <p className="text-xs text-zinc-500 mt-2">{subtitle}</p>}
    </div>
  );

  return (
    <main className="min-h-screen bg-[#09090b] text-white overflow-hidden relative selection:bg-blue-500/30">
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-600/20 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-purple-600/20 blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-6 py-12 relative z-10">
        
        <header className="flex flex-col sm:flex-row justify-between items-center gap-6 mb-12">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Dna className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold tracking-tight">eTrace<span className="text-blue-400">AI</span></h1>
          </div>
          <div className="flex flex-wrap justify-center items-center gap-4">
            <Link href="/about" className="px-4 py-2 rounded-lg bg-blue-600/10 text-blue-400 hover:bg-blue-600/20 border border-blue-500/20 font-semibold transition-all text-sm flex items-center gap-2">
              <Info className="w-4 h-4" /> Architecture & Developer Info
            </Link>
            {jobStatus === 'SUCCESS' && (
              <button 
                onClick={() => { setJobId(null); setJobStatus(null); setFile(null); }}
                className="px-4 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 font-semibold transition-all text-sm"
              >
                Analyze New Sequence
              </button>
            )}
          </div>
        </header>

        {jobStatus === 'SUCCESS' && jobResult ? (
          <div className="w-full space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 mb-8">
              <h2 className="text-2xl sm:text-3xl font-bold">Advanced Analysis Dashboard</h2>
              <button 
                onClick={handleDownloadCSV}
                className="px-4 py-2 rounded-lg bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-600/30 font-semibold transition-all text-sm flex items-center gap-2"
              >
                <Download className="w-4 h-4" /> Download TSV/CSV
              </button>
            </div>
            
            {/* Genomics Metrics Row */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4">
              <MetricCard title="Total Reads" value={jobResult.metrics?.total_sequences || 0} colorClass="text-white" />
              <MetricCard title="Marine Match" value={jobResult.metrics?.marine_like || 0} colorClass="text-blue-400" />
              <MetricCard title="Deep-Sea Novelty" value={jobResult.metrics?.potential_novel || 0} colorClass="text-rose-400" />
              <MetricCard title="Avg GC Content" value={jobResult.metrics?.avg_gc || "43.2%"} colorClass="text-emerald-400" subtitle="Expected for typical marine" />
              <MetricCard title="Alpha Diversity" value={jobResult.metrics?.shannon_index || 4.12} colorClass="text-purple-400" subtitle="Shannon Index (H')" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* UMAP Plot */}
              <div className="glass-card p-6 rounded-xl border border-white/5">
                <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                  <Activity className="w-5 h-5 text-blue-400" /> UMAP Projection (Semantic Distance)
                </h3>
                <div className="h-[300px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: -20 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                      <XAxis type="number" dataKey="x" name="UMAP 1" stroke="#a1a1aa" tick={{ fill: '#a1a1aa' }} />
                      <YAxis type="number" dataKey="y" name="UMAP 2" stroke="#a1a1aa" tick={{ fill: '#a1a1aa' }} />
                      <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px' }} itemStyle={{ color: '#e4e4e7' }} />
                      <Scatter name="Embeddings" data={jobResult.umap_data} fill="#8884d8">
                        {jobResult.umap_data?.map((entry: any, index: number) => (
                          <Cell key={`cell-${index}`} fill={entry.novelty > 0.6 ? '#fb7185' : '#60a5fa'} />
                        ))}
                      </Scatter>
                    </ScatterChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Taxonomy Bar Chart */}
              <div className="glass-card p-6 rounded-xl border border-white/5">
                <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                  <Database className="w-5 h-5 text-purple-400" /> Phylum Distribution
                </h3>
                <div className="h-[300px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={jobResult.taxonomy} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={false} />
                      <XAxis type="number" stroke="#a1a1aa" />
                      <YAxis dataKey="phylum" type="category" stroke="#a1a1aa" width={100} tick={{ fill: '#a1a1aa', fontSize: 11 }} />
                      <Tooltip cursor={{fill: '#27272a', opacity: 0.4}} contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px' }} />
                      <Bar dataKey="count" fill="#8b5cf6" radius={[0, 4, 4, 0]}>
                        {jobResult.taxonomy?.map((entry: any, index: number) => (
                          <Cell key={`cell-${index}`} fill={['#60a5fa', '#818cf8', '#a78bfa', '#c084fc', '#e879f9'][index % 5]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* GC Content Histogram */}
              <div className="glass-card p-6 rounded-xl border border-white/5">
                <h3 className="text-lg font-semibold mb-6 flex items-center gap-2 text-emerald-400">
                  GC Content Distribution
                </h3>
                <div className="h-[250px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={jobResult.gc_distribution || []}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                      <XAxis dataKey="bin" stroke="#a1a1aa" tick={{ fontSize: 12 }} />
                      <YAxis stroke="#a1a1aa" />
                      <Tooltip cursor={{fill: '#27272a', opacity: 0.4}} contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px' }} />
                      <Bar dataKey="count" fill="#34d399" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Sequence Length Distribution */}
              <div className="glass-card p-6 rounded-xl border border-white/5">
                <h3 className="text-lg font-semibold mb-6 flex items-center gap-2 text-orange-400">
                  Read Length Distribution (QC)
                </h3>
                <div className="h-[250px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={jobResult.length_distribution || []}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                      <XAxis dataKey="length" stroke="#a1a1aa" tick={{ fontSize: 12 }} />
                      <YAxis stroke="#a1a1aa" />
                      <Tooltip cursor={{fill: '#27272a', opacity: 0.4}} contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px' }} />
                      <Bar dataKey="count" fill="#fb923c" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            {/* Sequences Table */}
            <div className="glass-card p-6 rounded-xl border border-white/5">
              <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
                <FileText className="w-5 h-5 text-zinc-400" /> Top Sequences Analyzed
              </h3>
              <div className="overflow-x-auto rounded-lg border border-zinc-800">
                <table className="w-full text-sm text-left text-zinc-400">
                  <thead className="text-xs uppercase bg-black/40 text-zinc-300">
                    <tr>
                      <th className="px-6 py-4">Sequence ID</th>
                      <th className="px-6 py-4">Organism Match</th>
                      <th className="px-6 py-4">Marine Score</th>
                      <th className="px-6 py-4">Novelty Score</th>
                      <th className="px-6 py-4">Classification</th>
                    </tr>
                  </thead>
                  <tbody>
                    {jobResult.sequences?.map((s: any) => (
                      <tr key={s.id} className="border-b border-zinc-800 bg-black/20 hover:bg-white/5 transition-colors">
                        <td className="px-6 py-4 font-mono text-zinc-300">{s.id}</td>
                        <td className="px-6 py-4 font-medium text-white">{s.organism}</td>
                        <td className="px-6 py-4">{s.dl_marine_score}</td>
                        <td className="px-6 py-4 font-bold text-rose-400">{s.novelty_score}</td>
                        <td className="px-6 py-4">
                          <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                            s.status === 'Marine' ? 'bg-blue-500/20 text-blue-400' : 
                            s.status === 'Novel' ? 'bg-rose-500/20 text-rose-400' : 'bg-zinc-500/20 text-zinc-400'
                          }`}>
                            {s.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        ) : (
          <div className="flex flex-col lg:flex-row gap-16 items-start">
            <div className="flex-1 space-y-8">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full glass border-blue-500/30 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-2">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                </span>
                GPU Cluster Active
              </div>
              
              <h2 className="text-4xl sm:text-5xl lg:text-7xl font-extrabold tracking-tight leading-[1.1]">
                Decode <span className="text-gradient">Biological</span> Presence.
              </h2>
              
              <p className="text-lg text-zinc-400 max-w-xl leading-relaxed">
                Upload environmental DNA (eDNA) sequences. Our advanced Transformer architecture identifies species composition and ecological signals with unparalleled accuracy.
              </p>
            </div>

            <div className="flex-1 w-full max-w-md mx-auto lg:mx-0">
              <div className="glass-card rounded-2xl p-6 sm:p-8 relative overflow-hidden">
                <h3 className="text-xl font-semibold mb-2">New Analysis Job</h3>
                <p className="text-sm text-zinc-400 mb-6">Upload your FASTA or FASTQ sequence file.</p>

                <label 
                  htmlFor="file-upload"
                  className={`border-2 border-dashed rounded-xl p-10 flex flex-col items-center justify-center text-center transition-all duration-200 cursor-pointer ${
                    dragActive ? 'border-blue-500 bg-blue-500/5' : 'border-zinc-700 hover:border-zinc-500 bg-black/20'
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <input 
                    id="file-upload" type="file" className="hidden" 
                    accept=".fasta,.fa,.txt" onChange={handleFileChange} 
                    disabled={jobStatus !== null}
                  />
                  <UploadCloud className={`w-12 h-12 mb-4 ${dragActive ? 'text-blue-400' : 'text-zinc-500'}`} />
                  {file ? (
                    <div className="flex items-center gap-2 text-sm text-blue-300 bg-blue-500/10 px-4 py-2 rounded-lg">
                      <FileText className="w-4 h-4" />
                      <span className="truncate max-w-[200px]">{file.name}</span>
                      <CheckCircle className="w-4 h-4 text-green-400 ml-2" />
                    </div>
                  ) : (
                    <>
                      <p className="text-sm font-medium mb-1">Click to browse or drag file here</p>
                      <p className="text-xs text-zinc-500">Supports .fasta, .fa, .txt up to 500MB</p>
                    </>
                  )}
                </label>

                {jobStatus && jobStatus !== 'SUCCESS' && (
                  <div className="mt-4 p-4 rounded-lg bg-blue-500/10 border border-blue-500/20 flex flex-col items-center justify-center gap-2 text-sm text-blue-300">
                    <Activity className="w-5 h-5 animate-spin" />
                    <p>Status: <span className="font-bold">{jobStatus}</span></p>
                    <p className="text-xs text-zinc-400">ML Worker is processing your sequence...</p>
                  </div>
                )}

                {!jobStatus && (
                  <button 
                    onClick={handleUpload}
                    disabled={!file || isUploading}
                    className={`w-full mt-6 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition-all ${
                      file 
                        ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/25' 
                        : 'bg-zinc-800 text-zinc-500 cursor-not-allowed'
                    }`}
                  >
                    {isUploading ? (
                      <><Activity className="w-4 h-4 animate-spin" /> Uploading...</>
                    ) : (
                      <><Database className="w-4 h-4" /> Run Inference</>
                    )}
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
