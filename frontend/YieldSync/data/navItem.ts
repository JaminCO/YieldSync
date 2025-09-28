import { NavItem } from "@/types/types";

export const navItem: NavItem[] = [
  {
    id: 1,
    image: '/dashboard-icon.svg',
    name: 'Dashboard',
    href: '/dashboard'
  },
  {
    id: 2,
    image: '/wallet-icon.svg',
    name: 'Wallets',
    href: '/dashboard/wallet'
  },
  {
    id: 3,
    image: '/pools-icon.svg',
    name: 'Pools',
    href: '/dashboard/pools'
  },
   {
     id: 5,
     image : '/pools-icon.svg',
     name: 'Recommendations',
     href: '/dashboard/recommendations'
  },
  {
     id: 4,
     image : '/settings-icon.svg',
     name: 'Settings',
     href: '/dashboard/settings'
  },
 
]