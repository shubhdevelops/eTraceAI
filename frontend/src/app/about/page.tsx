import Link from 'next/link';
import { ArrowLeft, Cpu, Server, Network, ShieldCheck, Zap, Dna, Code } from 'lucide-react';

export default function AboutPage() {
  return (
    <main className="min-h-screen bg-[#09090b] text-white overflow-hidden relative selection:bg-blue-500/30">
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-600/20 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-purple-600/20 blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-6 py-12 relative z-10">
        
        {/* Navigation */}
        <header className="flex justify-between items-center mb-16">
          <Link href="/" className="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors group">
            <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
            <span className="font-medium">Back to Analyzer</span>
          </Link>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Dna className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold tracking-tight">eTrace<span className="text-blue-400">AI</span></h1>
          </div>
        </header>

        {/* Developer Section */}
        <section className="mb-24">
          <div className="glass-card rounded-3xl p-10 md:p-14 relative overflow-hidden border border-white/10">
            <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl" />
            
            <div className="flex flex-col md:flex-row gap-10 items-center relative z-10">
              <div className="flex-1">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-6">
                  <Code className="w-4 h-4" /> Lead Architect
                </div>
                <h2 className="text-4xl md:text-5xl font-extrabold mb-4 tracking-tight">Shubham Thakur</h2>
                <p className="text-xl text-zinc-300 mb-6 font-medium">Smart India Hackathon (SIH) Grand Finalist — Team CRISPR_CREW</p>
                <p className="text-zinc-400 leading-relaxed max-w-2xl">
                  What started as an innovative deep-sea biodiversity prototype for the Smart India Hackathon has now been entirely re-architected into a robust, production-grade microservices platform. My focus was not just on building an AI model, but designing an enterprise-ready infrastructure capable of handling intensive bioinformatics workloads efficiently.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Architecture Evolution */}
        <section className="mb-24">
          <h2 className="text-3xl font-bold mb-10 text-center tracking-tight">The Evolution: Prototype to Production</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* V1: SIH Prototype */}
            <div className="glass-card rounded-2xl p-8 border border-rose-500/20 bg-rose-500/5 relative">
              <div className="absolute top-4 right-4 text-xs font-bold px-3 py-1 bg-rose-500/20 text-rose-300 rounded-full">v1.0 (SIH Prototype)</div>
              <h3 className="text-xl font-bold mb-4 text-rose-200">Monolithic Architecture</h3>
              <ul className="space-y-4 text-zinc-400">
                <li className="flex gap-3"><span className="text-rose-400">✖</span> <span><strong>Single Process:</strong> Streamlit handled UI, file uploads, AND heavy AI inference simultaneously, causing browser freezes.</span></li>
                <li className="flex gap-3"><span className="text-rose-400">✖</span> <span><strong>Synchronous Execution:</strong> Large FASTA files would timeout the HTTP connection before processing finished.</span></li>
                <li className="flex gap-3"><span className="text-rose-400">✖</span> <span><strong>Static UI:</strong> Visualizations were generated as static PNG images in the backend.</span></li>
              </ul>
            </div>

            {/* V2: Production Grade */}
            <div className="glass-card rounded-2xl p-8 border border-green-500/20 bg-green-500/5 relative shadow-[0_0_40px_rgba(34,197,94,0.1)]">
              <div className="absolute top-4 right-4 text-xs font-bold px-3 py-1 bg-green-500/20 text-green-300 rounded-full">v2.0 (Production-Ready)</div>
              <h3 className="text-xl font-bold mb-4 text-green-200">Decoupled Microservices</h3>
              <ul className="space-y-4 text-zinc-400">
                <li className="flex gap-3"><span className="text-green-400">✔</span> <span><strong>Asynchronous Workers:</strong> A dedicated Redis + Celery worker queue offloads AI inference, ensuring the API is never blocked.</span></li>
                <li className="flex gap-3"><span className="text-green-400">✔</span> <span><strong>Modern Tech Stack:</strong> React + Next.js frontend communicating with a high-performance FastAPI backend.</span></li>
                <li className="flex gap-3"><span className="text-green-400">✔</span> <span><strong>Interactive Rendering:</strong> UMAP clustering and taxonomic plots are now rendered dynamically in the browser using Recharts.</span></li>
                <li className="flex gap-3"><span className="text-green-400">✔</span> <span><strong>Dockerized Deployment:</strong> Fully containerized environment for seamless cloud deployment.</span></li>
              </ul>
            </div>
          </div>
        </section>

        {/* Feature Uniqueness */}
        <section>
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight mb-4">What Makes eTraceAI Unique?</h2>
            <p className="text-zinc-400 max-w-2xl mx-auto">Key architectural and scientific differentiators to highlight during technical interviews.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="glass-card p-6 rounded-xl border border-blue-500/20 hover:border-blue-500/40 transition-colors group">
              <div className="w-12 h-12 rounded-lg bg-blue-500/20 flex items-center justify-center mb-4 text-blue-400 group-hover:scale-110 transition-transform">
                <Network className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold mb-2">Deep DNA Embeddings</h3>
              <p className="text-sm text-zinc-400 leading-relaxed">
                Instead of basic exact-match searches (like BLAST), we use Transformer-based sequence representations. This captures semantic biological meaning, allowing us to project sequences into a 2D UMAP space to discover entirely novel species that share structural similarities.
              </p>
            </div>

            <div className="glass-card p-6 rounded-xl border border-purple-500/20 hover:border-purple-500/40 transition-colors group">
              <div className="w-12 h-12 rounded-lg bg-purple-500/20 flex items-center justify-center mb-4 text-purple-400 group-hover:scale-110 transition-transform">
                <Server className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold mb-2">Non-Blocking Architecture</h3>
              <p className="text-sm text-zinc-400 leading-relaxed">
                Bioinformatics workflows take minutes to hours. This platform is built specifically for long-running AI jobs using the producer-consumer pattern (FastAPI → Redis → Celery). The frontend actively polls job status via WebSockets/REST, delivering an enterprise-tier UX.
              </p>
            </div>

            <div className="glass-card p-6 rounded-xl border border-emerald-500/20 hover:border-emerald-500/40 transition-colors group">
              <div className="w-12 h-12 rounded-lg bg-emerald-500/20 flex items-center justify-center mb-4 text-emerald-400 group-hover:scale-110 transition-transform">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold mb-2">Scalable Infrastructure</h3>
              <p className="text-sm text-zinc-400 leading-relaxed">
                By decoupling the frontend from the ML execution engine, we can horizontally scale the `ml_worker` containers independently based on GPU demand, without affecting the lightweight frontend or API gateway. It's ready for Kubernetes orchestration.
              </p>
            </div>
          </div>
        </section>

      </div>
    </main>
  );
}
