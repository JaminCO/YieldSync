'use client'
import React, { useState } from 'react';
import { Wallet, Shield, Zap, ArrowRight, Check,  } from 'lucide-react';


const ConnectWallet = () => {
  const [connecting, setConnecting] = useState<string | null>(null);
  const [connected, setConnected] = useState(false);
  const [connectedWallet, setConnectedWallet] = useState<{
    id: string;
    name: string;
    description: string;
    icon: string;
    popular: boolean;
    color: string;
  } | null>(null);

  const wallets = [
    {
      id: 'metamask',
      name: 'MetaMask',
      description: 'Connect using MetaMask wallet',
      icon: '🦊',
      popular: true,
      color: 'from-orange-500 to-red-500'
    },
    {
      id: 'walletconnect',
      name: 'WalletConnect',
      description: 'Scan with WalletConnect to connect',
      icon: '🔗',
      popular: false,
      color: 'from-blue-500 to-purple-500'
    },
    {
      id: 'coinbase',
      name: 'Coinbase Wallet',
      description: 'Connect using Coinbase Wallet',
      icon: '🏦',
      popular: true,
      color: 'from-blue-600 to-blue-700'
    },
    {
      id: 'phantom',
      name: 'Phantom',
      description: 'Connect using Phantom wallet',
      icon: '👻',
      popular: false,
      color: 'from-purple-500 to-pink-500'
    },
    {
      id: 'trustwallet',
      name: 'Trust Wallet',
      description: 'Connect using Trust Wallet',
      icon: '🛡️',
      popular: false,
      color: 'from-cyan-500 to-blue-500'
    },
    {
      id: 'rainbow',
      name: 'Rainbow',
      description: 'Connect using Rainbow wallet',
      icon: '🌈',
      popular: false,
      color: 'from-pink-500 to-yellow-500'
    }
  ];

  const handleConnect = async (walletId: string) => {
    setConnecting(walletId);
    
    // Simulate connection process
    setTimeout(() => {
      setConnecting(null);
      setConnected(true);
      const foundWallet = wallets.find(w => w.id === walletId);
      setConnectedWallet(foundWallet || null);
    }, 2000);
  };

  const handleDisconnect = () => {
    setConnected(false);
    setConnectedWallet(null);
  };

  if (connected) {
    return (

      <div className="min-h-screen flex items-center justify-center p-4 " style={{background: 'linear-gradient(135deg, #001437 0%, #002855 50%, #001437 100%)'}}>
      
        <div className="bg-white/5 mt-10 backdrop-blur-3xl rounded-3xl p-8 max-w-md w-full border border-white/10 shadow-[0_8px_32px_0_rgba(31,38,135,0.37)]">
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 bg-green-500 rounded-full flex items-center justify-center">
              <Check className="w-8 h-8 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">Wallet Connected!</h2>
            <p className="text-gray-300 mb-6">Successfully connected to {connectedWallet?.name}</p>
            
            <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-4 mb-6 border border-white/10">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{connectedWallet?.icon}</span>
                  <div className="text-left">
                    <p className="text-white/90 font-semibold">{connectedWallet?.name}</p>
                    <p className="text-white/60 text-sm">0x1234...5678</p>
                  </div>
                </div>
                <div className="w-3 h-3 bg-emerald-400 rounded-full shadow-[0_0_10px_rgba(52,211,153,0.5)]"></div>
              </div>
            </div>

            <button
              onClick={handleDisconnect}
              className="w-full py-3 px-6 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-xl transition-all duration-200 transform hover:scale-105"
            >
              Disconnect Wallet
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
          <div className="min-h-screen flex items-center justify-center p-4" style={{background: 'linear-gradient(135deg, #001437 0%, #002855 50%, #001437 100%)'}}>
            
      <div className="bg-white/5 mt-20 backdrop-blur-3xl rounded-3xl p-8 max-w-md w-full border border-white/10 shadow-[0_8px_32px_0_rgba(31,38,135,0.37)]">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-cyan-400/20 to-blue-600/20 backdrop-blur-sm rounded-2xl flex items-center justify-center border border-white/20">
            <Wallet className="w-8 h-8 text-cyan-300" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Connect Wallet</h1>
          <p className="text-gray-400">Choose your preferred wallet to connect to the app</p>
        </div>

        {/* Security Features */}
        <div className="grid grid-cols-2 gap-3 mb-8">
          <div className="bg-white/5 backdrop-blur-sm rounded-xl p-3 border border-white/10">
            <Shield className="w-5 h-5 text-emerald-400 mb-1" />
            <p className="text-white/90 text-sm font-medium">Secure</p>
            <p className="text-white/60 text-xs">End-to-end encrypted</p>
          </div>
          <div className="bg-white/5 backdrop-blur-sm rounded-xl p-3 border border-white/10">
            <Zap className="w-5 h-5 text-amber-400 mb-1" />
            <p className="text-white/90 text-sm font-medium">Fast</p>
            <p className="text-white/60 text-xs">Instant connection</p>
          </div>
        </div>

        {/* Wallet Options */}
        <div className="space-y-3">
          {wallets.map((wallet) => (
            <button
              key={wallet.id}
              onClick={() => handleConnect(wallet.id)}
              disabled={connecting === wallet.id}
              className="w-full p-4 bg-white/5 backdrop-blur-sm hover:bg-white/10 border border-white/10 hover:border-white/20 rounded-xl transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed group shadow-[0_4px_16px_0_rgba(31,38,135,0.15)]"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="relative">
                    <span className="text-2xl block">{wallet.icon}</span>
                    {wallet.popular && (
                      <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-white/20"></div>
                    )}
                  </div>
                  <div className="text-left">
                    <div className="flex items-center space-x-2">
                      <p className="text-white font-semibold">{wallet.name}</p>
                      {wallet.popular && (
                        <span className="bg-emerald-400/20 backdrop-blur-sm text-emerald-300 text-xs px-2 py-0.5 rounded-full font-medium border border-emerald-400/30">
                          Popular
                        </span>
                      )}
                    </div>
                    <p className="text-gray-400 text-sm">{wallet.description}</p>
                  </div>
                </div>
                
                {connecting === wallet.id ? (
                  <div className="w-6 h-6 border-2 border-white/20 border-t-cyan-400 rounded-full animate-spin"></div>
                ) : (
                  <ArrowRight className="w-5 h-5 text-white/40 group-hover:text-cyan-300 transition-colors duration-300" />
                )}
              </div>
            </button>
          ))}
        </div>

        {/* Footer */}
        {/* <div className="mt-8 pt-6 border-t border-white/10">
          <p className="text-center text-white/50 text-sm">
            By connecting, you agree to our{' '}
            <a href="#" className="text-cyan-300 hover:text-cyan-200 transition-colors">
              Terms of Service
            </a>{' '}
            and{' '}
            <a href="#" className="text-cyan-300 hover:text-cyan-200 transition-colors">
              Privacy Policy
            </a>
          </p>
        </div> */}
      </div>
    </div>
  );
};

export default ConnectWallet;