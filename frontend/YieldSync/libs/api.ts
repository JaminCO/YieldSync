const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  private getAuthToken() {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    return token ? `Bearer ${token}` : null;
  }

  async get(endpoint: string) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

    async auth_get(endpoint: string, token: string) {
    const authToken = this.getAuthToken();
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': authToken || `Bearer ${token}`,
        },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }


  async post(endpoint: string, data: any) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const jsonResponse = await response.json();
    return jsonResponse;
  }

    async auth_post(endpoint: string, data: any, token: string) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(data),
        });
        if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonResponse = await response.json();
        return jsonResponse;
    }

  // Health check
  async healthCheck() {
    return this.get('/health');
  }

  // User endpoints
  async getUser(token: string) {
    return this.auth_get('/users/me', token);
  }

  async createUser(userData: any) {
    return this.post('/users/signup', userData);
  }

  // Wallet endpoints
  async getWallets(token: string) {
    return this.auth_get('/wallets/me', token);
  }

  async createWallet(walletData: any, token: string) {
    return this.auth_post('/wallets/me', walletData, token);
  }

  // Pool endpoints
  async getPools() {
    return this.get('/pools');
  }
}

export const apiClient = new ApiClient();
