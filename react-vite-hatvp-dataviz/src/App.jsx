import { BrowserRouter, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import OrganizationMentions from './pages/OrganizationMentions';
import AgeDistribution from './pages/AgeDistribution';
import GenderDistribution from './pages/GenderDistribution';
import DelayByMandate from './pages/DelayByMandate';
import About from './pages/About';

function App() {
  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen">
        <NavBar />
        <main className="flex-grow p-4">
          <Routes>
            <Route path="/" element={<OrganizationMentions />} />
            <Route path="/age" element={<AgeDistribution />} />
            <Route path="/gender" element={<GenderDistribution />} />
            <Route path="/delay" element={<DelayByMandate />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
