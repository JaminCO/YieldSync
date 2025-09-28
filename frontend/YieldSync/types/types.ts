 export interface AboutInfo {
  id: number,
  header: string,
  answer: string
}

export interface ValueInfo {
  id: number,
  value: string,
  body: string
}

export interface FounderInfo {
  id: number,
  image: string,
  name: string,
  position: string,
  bio: string,
  githubLink: string,
  linkedinLink: string

}

export interface NavItem {
  id: number,
  image: string
  name: string,
  href: string
}

export interface Summary {
  id: number,
  name: string,
  value:string,
  money: boolean
}

export interface RecommendInfo {
  id: number,
  name: string,
  risk: string

}

export interface SupportedChainInfo {
  id:number,
  image:string,
  name:string
}

export interface PoolsTableInfo {
  id: number,
  pool: string,
  estimatedAPY: number,
  riskScore: string,
  summary: string
}