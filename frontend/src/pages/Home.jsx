import { Link } from 'react-router-dom';
import { Shield, Search, CheckCircle, TrendingUp, ArrowRight, Sparkles } from 'lucide-react';

const Home = () => {
  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <header className="border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-cyan-400 via-purple-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">TruthLens</h1>
                <p className="text-xs text-slate-500">AI Fact Checker</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Link 
                to="/login" 
                className="px-4 py-2 text-slate-300 hover:text-white transition"
              >
                Sign In
              </Link>
              <Link 
                to="/register" 
                className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-purple-500 text-white rounded-xl font-medium hover:shadow-lg hover:shadow-purple-500/30 transition"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-500/10 border border-purple-500/30 rounded-full text-purple-400 text-sm mb-8">
            <Sparkles className="w-4 h-4" />
            AI-Powered Misinformation Detection
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
            Detect Fake News with{' '}
            <span className="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              AI Precision
            </span>
          </h1>
          
          <p className="text-xl text-slate-400 mb-10 max-w-2xl mx-auto">
            TruthLens uses advanced BERT AI models to analyze news articles and detect misinformation with high accuracy. Verify before you share.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/register" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-cyan-500 to-purple-500 text-white rounded-xl font-medium text-lg hover:shadow-xl hover:shadow-purple-500/30 transition"
            >
              Start Checking News
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link 
              to="/login" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-slate-800 text-white rounded-xl font-medium text-lg hover:bg-slate-700 transition border border-slate-700"
            >
              Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-4 border-t border-slate-800">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-white text-center mb-12">
            How It Works
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 bg-slate-800/50 rounded-2xl border border-slate-700">
              <div className="w-12 h-12 bg-cyan-500/20 rounded-xl flex items-center justify-center mb-4">
                <Search className="w-6 h-6 text-cyan-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Paste Any News</h3>
              <p className="text-slate-400">
                Simply paste any news article or claim you want to verify into our analyzer.
              </p>
            </div>
            
            <div className="p-6 bg-slate-800/50 rounded-2xl border border-slate-700">
              <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mb-4">
                <TrendingUp className="w-6 h-6 text-purple-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">AI Analysis</h3>
              <p className="text-slate-400">
                Our fine-tuned BERT model analyzes patterns to detect misinformation.
              </p>
            </div>
            
            <div className="p-6 bg-slate-800/50 rounded-2xl border border-slate-700">
              <div className="w-12 h-12 bg-green-500/20 rounded-xl flex items-center justify-center mb-4">
                <CheckCircle className="w-6 h-6 text-green-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Get Results</h3>
              <p className="text-slate-400">
                Receive instant results with confidence scores and source verification.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-20 px-4 border-t border-slate-800">
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-3 gap-8 text-center">
            <div>
              <p className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">95%</p>
              <p className="text-slate-400 mt-2">Accuracy Rate</p>
            </div>
            <div>
              <p className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">50K+</p>
              <p className="text-slate-400 mt-2">Articles Analyzed</p>
            </div>
            <div>
              <p className="text-4xl font-bold bg-gradient-to-r from-pink-400 to-cyan-400 bg-clip-text text-transparent">&lt;2s</p>
              <p className="text-slate-400 mt-2">Analysis Time</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-slate-800">
        <div className="max-w-6xl mx-auto text-center text-slate-500">
          <p>© 2025 TruthLens. AI-Powered Fake News Detection.</p>
        </div>
      </footer>
    </div>
  );
};

export default Home;
