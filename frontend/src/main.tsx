import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

// Import API override and test utilities for development
if (import.meta.env.DEV) {
  // This will override the real API with mock implementations
  import('./lib/api-override')
    .then(() => console.log('API override loaded'))
    .catch(err => console.error('Failed to load API override:', err))
  
  // Import test utilities for the mock API
  import('./lib/test-mock-api')
    .then(() => console.log('Mock API test utilities loaded. Use window.testMockApi() to test.'))
    .catch(err => console.error('Failed to load mock API test utilities:', err))
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
