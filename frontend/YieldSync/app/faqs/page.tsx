'use client';

import { useState } from 'react';
import NavBar from '../components/NavBar';

// FAQ data
const faqs = [
  {
    question: 'What is DeFi?',
    answer:
      'DeFi (Decentralized Finance) is a financial system built on blockchains like Ethereum, where anyone can lend, borrow, trade, or earn interest on crypto without banks or intermediaries.',
  },
  {
    question: 'What are pools?',
    answer:
      'Pools are smart contracts where users deposit crypto assets together for a purpose — like staking, lending, or providing liquidity — and earn rewards or interest in return.',
  },
  {
    question: 'How does YieldSync choose pools?',
    answer: (
      <div>
        <p>
          YieldSync aggregates pools across multiple blockchains via APIs like
          DeFiLlama, then applies a ranking system. Pools are scored by:
        </p>
        <ul className="list-disc list-inside mt-2 space-y-1">
          <li>APY (yields & rewards)</li>
          <li>TVL (size & stability)</li>
          <li>Risk factors (impermanent loss, volatility, liquidity)</li>
          <li>AI predictions for stability & growth</li>
        </ul>
      </div>
    ),
  },
  {
    question: 'What is YieldSync?',
    answer:
      'YieldSync is an AI-powered platform that helps investors discover, compare, and manage yield farming opportunities across DeFi. It aggregates pool data, assigns risk scores, and provides human-readable insights — all in one dashboard.',
  },
  {
    question: 'What Is Yield Farming?',
    answer:
      'Yield farming is the practice of earning rewards or interest by putting your crypto into DeFi protocols — like staking ETH, lending stablecoins, or providing liquidity on DEXs.',
  },
  {
    question: 'Is YieldSync Free?',
    answer: (
      <p>Yes, YieldSync will offer a free tier for basic pool discovery. Advanced features (like AI insights, risk analytics, and strategy backtesting) will be available in a <b>premium subscription.</b></p>),
  },
];

export default function FAQPage() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const toggle = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <>
      <NavBar />
      <main className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden p-6 md:p-12 duration-1000 pt-40">

        
        <div className="absolute -top-20 left-1/3 w-[600px] h-[600px] -z-10 bg-gradient-to-tr from-blue-500/30 to-transparent rounded-full blur-3xl opacity-70" />
        <div className="absolute bottom-0 right-1/4 w-[400px] h-[400px] -z-10 bg-gradient-to-br from-blue-400/40 to-transparent rounded-full blur-2xl opacity-60" />

        {/* Accordion */}
        <div className="relative z-10 max-w-3xl w-full -mt-33 p-6 md:p-8 bg-white/100 dark:bg-zinc-900/50 rounded-3xl shadow-xl backdrop-blur-md">
          <h2 className="mb-8 text-center text-2xl font-bold dark:text-white md:text-3xl">
            Frequently Asked Questions
          </h2>
          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <div
                key={index}
                
              >
                <div className="rounded-2xl bg-white dark:bg-zinc-800 shadow-md transition-all">
                  <button
                  onClick={() => toggle(index)}
                  className="w-full flex items-center justify-between px-4 py-3 text-left focus:outline-none"
                >
                  <span className="text-lg font-medium text-zinc-800 dark:text-white">
                    {faq.question}
                  </span> 
                  <span
                    className={`transform transition-transform ${
                      openIndex === index ? 'rotate-180' : ''
                    }`}
                  >
                    ▼
                  </span>
                </button>
                </div>
                
                {openIndex === index && (
                  <div className="px-6 mt-3 ml-7 pt-3 rounded-2xl dark:bg-zinc-700 pb-4 text-zinc-700 dark:text-zinc-200">
                    {faq.answer}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </main>
    </>
  );
}
