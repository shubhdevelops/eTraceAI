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

        {/* Interview Defense & Technical Deep Dive */}
        <section>
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight mb-4">Technical Interview Defense Guide</h2>
            <p className="text-zinc-400 max-w-2xl mx-auto">Key architectural concepts, design decisions, and common interview questions tackled during the platform's evolution.</p>
          </div>

          <div className="space-y-8">
            {/* Topic 1: Message Queues & Microservices */}
            <div className="glass-card p-8 rounded-xl border border-blue-500/20">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 rounded-lg bg-blue-500/20 flex items-center justify-center text-blue-400">
                  <Server className="w-6 h-6" />
                </div>
                <h3 className="text-2xl font-bold">Why Redis & Celery? (Producer-Consumer Pattern)</h3>
              </div>
              <p className="text-zinc-300 leading-relaxed mb-6">
                <strong>The Problem:</strong> ML inference (processing 500MB FASTA files through a Transformer model) takes a long time. If the FastAPI server handles this synchronously, the HTTP request will timeout, the server will block other users, and the UI will freeze.
              </p>
              <p className="text-zinc-300 leading-relaxed mb-6">
                <strong>The Solution:</strong> I implemented a <em>Producer-Consumer</em> architecture. 
                <br />1. The <strong>Producer</strong> (FastAPI) receives the file, saves it, and immediately pushes a "Job Ticket" to Redis. It replies to the user in milliseconds: "Job Queued."
                <br />2. The <strong>Message Broker</strong> (Redis) safely stores the queue of jobs in memory.
                <br />3. The <strong>Consumer</strong> (Celery Worker), which has access to the GPU, constantly pulls jobs from Redis, processes them, and writes the results back to Redis.
              </p>
              <div className="bg-black/30 p-4 rounded-lg border border-white/5">
                <p className="text-sm font-semibold text-blue-400 mb-2">Q: "What happens if the Celery worker crashes during inference?"</p>
                <p className="text-sm text-zinc-400">A: Because Redis retains the state, we can configure Celery to acknowledge the task <em>only after</em> it succeeds (using `acks_late=True`). If the worker crashes, the task is returned to the queue, and another worker (or the restarted worker) will pick it up, guaranteeing no data loss.</p>
              </div>
            </div>

            {/* Topic 2: Prototype to Production */}
            <div className="glass-card p-8 rounded-xl border border-purple-500/20">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 rounded-lg bg-purple-500/20 flex items-center justify-center text-purple-400">
                  <Network className="w-6 h-6" />
                </div>
                <h3 className="text-2xl font-bold">Prototype to Production: What Changed?</h3>
              </div>
              <ul className="space-y-4 text-zinc-300 list-disc pl-5 mb-6">
                <li><strong>State Management:</strong> In the prototype (Streamlit), state was held in the browser session. Now, state is strictly managed on the server via `job_id` polling. The frontend is completely stateless, making it infinitely scalable.</li>
                <li><strong>Decoupling UI from Compute:</strong> Previously, if the Python script crashed due to OOM (Out of Memory) on the GPU, the entire website went down. Now, if the ML Worker crashes, the Next.js frontend and FastAPI gateway remain 100% operational, and the user simply sees a gracefully handled "Job Failed" status.</li>
                <li><strong>Client-Side Rendering (CSR):</strong> The old app generated static PNG plots on the server and sent them down. This wasted server CPU. Now, the server only sends raw JSON data. The client browser uses its own CPU to render interactive Recharts graphs, saving massive server costs.</li>
                <li><strong>Deployment Economics:</strong> The monolithic design required expensive servers because the web server needed a GPU. By decoupling, the frontend (Next.js) can be hosted on a free CDN (Vercel), the API (FastAPI) on a cheap CPU server, and only the Celery worker needs an expensive GPU instance.</li>
              </ul>
              <div className="bg-black/30 p-4 rounded-lg border border-white/5">
                <p className="text-sm font-semibold text-purple-400 mb-2">Q: "Why use Next.js if you aren't using Server-Side Rendering (SSR) for the plots?"</p>
                <p className="text-sm text-zinc-400">A: Next.js provides an incredibly robust API for routing and component structure, but more importantly, it allows us to deploy directly to Vercel's Edge Network. Even though the dashboard uses CSR (`use client`), the shell of the application is static, resulting in instantaneous page loads.</p>
              </div>
            </div>

            {/* Topic 3: AI Architecture */}
            <div className="glass-card p-8 rounded-xl border border-emerald-500/20">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 rounded-lg bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                  <Cpu className="w-6 h-6" />
                </div>
                <h3 className="text-2xl font-bold">The AI: Deep DNA Embeddings vs BLAST</h3>
              </div>
              <p className="text-zinc-300 leading-relaxed mb-6">
                <strong>Traditional Approach (BLAST):</strong> Bioinformatics tools historically rely on exact character-matching. If a sequence has mutated heavily, BLAST fails to recognize it because the letters don't align.
              </p>
              <p className="text-zinc-300 leading-relaxed mb-6">
                <strong>Our Approach (Transformers):</strong> We use a Deep Learning Transformer model that creates <em>embeddings</em> (high-dimensional vectors). The model learns the "grammar" of the DNA rather than just the spelling. This is why our UMAP projection works: sequences that are biologically similar (even if mutated) group together in the vector space, allowing us to detect completely novel deep-sea organisms that BLAST would ignore.
              </p>
              <div className="bg-black/30 p-4 rounded-lg border border-white/5">
                <p className="text-sm font-semibold text-emerald-400 mb-2">Q: "How do you handle the massive size of genomic datasets?"</p>
                <p className="text-sm text-zinc-400">A: Memory management is critical. We process FASTA files in generator chunks (streaming) rather than loading a 500MB file entirely into RAM. The ML inference is batched so we don't exceed GPU VRAM limits.</p>
              </div>
            </div>

          </div>
        </section>

      </div>
    </main>
  );
}
