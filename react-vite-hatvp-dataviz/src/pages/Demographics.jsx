import Diversity3Icon from '@mui/icons-material/Diversity3';
import { PageContainer } from '../components/Layout';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import AgeDistributionSection from '../components/demographics/AgeDistributionSection';
import AgePyramidSection from '../components/demographics/AgePyramidSection';
import GenderDistributionSection from '../components/demographics/GenderDistributionSection';

function Demographics() {
  return (
    <PageContainer>
      <Box sx={{
        display: 'flex',
        alignItems: 'center',
        gap: 2,
        mb: 2.5,
        p: 2,
        border: '1px solid',
        borderColor: 'divider',
        borderRadius: 2,
        bgcolor: 'background.paper',
        boxShadow: 'none',
        position: 'relative',
        '&::before': {
          content: '""',
          position: 'absolute',
          left: 0,
          top: 0,
          bottom: 0,
          width: 8,
          bgcolor: 'primary.main',
          borderTopLeftRadius: 8,
          borderBottomLeftRadius: 8,
        },
      }}>
        <Diversity3Icon color="primary" fontSize="large" />
        <Box>
          <Typography variant="h4" component="h1" sx={{ fontWeight: 800, lineHeight: 1.2 }}>
            Demographics Overview
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Age distribution, age pyramid, and gender split.
          </Typography>
        </Box>
      </Box>
      <AgeDistributionSection />
      <AgePyramidSection />
      <GenderDistributionSection />
    </PageContainer>
  );
}

export default Demographics;
