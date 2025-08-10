import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Box from '@mui/material/Box';
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import OrganizationMentions from './pages/OrganizationMentions';
import AgeDistribution from './pages/AgeDistribution';
import GenderDistribution from './pages/GenderDistribution';
import DelayByMandate from './pages/DelayByMandate';
import About from './pages/About';
import AgePyramid from './pages/AgePyramid';

function App() {
  return (
    <BrowserRouter>
      <Box display="flex" flexDirection="column" minHeight="100vh">
        <NavBar />
        <Box component="main" sx={{ flexGrow: 1, py: 3 }}>
          <Routes>
            <Route path="/" element={<OrganizationMentions />} />
            <Route path="/age" element={<AgeDistribution />} />
            <Route path="/pyramid" element={<AgePyramid />} />
            <Route path="/gender" element={<GenderDistribution />} />
            <Route path="/delay" element={<DelayByMandate />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </Box>
        <Footer />
      </Box>
    </BrowserRouter>
  );
}

export default App;
