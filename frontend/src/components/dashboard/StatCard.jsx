import React from 'react';
import { motion } from 'framer-motion';

const StatCard = React.memo(({ label, value, icon: Icon, color = 'blue', delay = 0 }) => {
  const colorMap = {
    blue: {
      bg: 'from-pro-blue/20 to-pro-blue/5',
      text: 'text-pro-blue',
      border: 'border-pro-blue/20',
      shadow: 'shadow-pro-blue/10',
      glow: 'from-pro-blue/20'
    },
    green: {
      bg: 'from-tech-lime/20 to-tech-lime/5',
      text: 'text-tech-lime',
      border: 'border-tech-lime/20',
      shadow: 'shadow-tech-lime/10',
      glow: 'from-tech-lime/20'
    },
    red: {
      bg: 'from-tech-rose/20 to-tech-rose/5',
      text: 'text-tech-rose',
      border: 'border-tech-rose/20',
      shadow: 'shadow-tech-rose/10',
      glow: 'from-tech-rose/20'
    },
  };

  const theme = colorMap[color] || colorMap.blue;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className={`relative group p-4 rounded-xl bg-pro-surface border border-pro-border overflow-hidden transition-all hover:border-pro-blue/30`}
    >
      {/* 3D Inner Shadow / Depth */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent pointer-events-none" />
      
      {/* Background Glow */}
      <div className={`absolute -right-6 -bottom-6 w-24 h-24 bg-gradient-to-br ${theme.glow} blur-[30px] opacity-20 group-hover:opacity-40 transition-opacity`} />

      <div className="relative flex items-center justify-between gap-3">
        <div className="flex-1 min-w-0">
          <p className="text-[9px] font-black text-pro-sub uppercase tracking-[0.15em] mb-0.5 truncate">
            {label}
          </p>
          <div className="flex items-baseline gap-1.5">
            <h3 className="text-2xl font-black text-pro-text tracking-tighter">
              {value}
            </h3>
            <span className={`text-[9px] font-bold ${theme.text} uppercase tracking-wider`}>
              Units
            </span>
          </div>
          {/* Metadata Readout */}
          <div className="mt-2.5 flex gap-2.5">
             <div className="flex items-center gap-1">
                <div className={`w-0.5 h-0.5 rounded-full ${theme.text} animate-pulse`} />
                <span className="text-[7px] font-bold text-pro-sub uppercase">Load: 12%</span>
             </div>
             <div className="flex items-center gap-1">
                <div className={`w-0.5 h-0.5 rounded-full ${theme.text} opacity-50`} />
                <span className="text-[7px] font-bold text-pro-sub uppercase">Parity: 0.98</span>
             </div>
          </div>
        </div>

        <div className={`w-11 h-11 rounded-lg bg-gradient-to-br ${theme.bg} border ${theme.border} flex items-center justify-center relative overflow-hidden group-hover:scale-110 transition-transform shrink-0`}>
           <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity" />
           <Icon className={`w-5 h-5 ${theme.text}`} />
           
           {/* Decorative elements */}
           <div className="absolute top-0.5 left-0.5 w-1 h-1 border-t border-l border-white/20" />
           <div className="absolute bottom-0.5 right-0.5 w-1 h-1 border-b border-r border-white/20" />
        </div>
      </div>

      {/* Progress Line Decoration */}
      <div className="absolute bottom-0 left-0 w-full h-[2px] bg-pro-border overflow-hidden">
        <motion.div 
          initial={{ x: '-100%' }}
          animate={{ x: '100%' }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear", delay: delay * 2 }}
          className={`w-1/3 h-full bg-gradient-to-r from-transparent via-current to-transparent ${theme.text}`}
        />
      </div>
    </motion.div>
  );
});

export default StatCard;
