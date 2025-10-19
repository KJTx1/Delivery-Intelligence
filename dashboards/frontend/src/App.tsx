import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import OperationsManagerDashboard from './pages/OperationsManager'
import DriverDashboard from './pages/Driver'
import CustomerServiceDashboard from './pages/CustomerService'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/operations" replace />} />
        
        <Route path="/operations" element={<OperationsManagerDashboard />} />
        
        <Route path="/driver" element={<DriverDashboard />} />
        
        <Route path="/cs" element={<CustomerServiceDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
