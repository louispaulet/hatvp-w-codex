import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import InsightsIcon from '@mui/icons-material/Insights';
import PeopleIcon from '@mui/icons-material/People';
import ScheduleIcon from '@mui/icons-material/Schedule';
import InfoIcon from '@mui/icons-material/Info';
import { Link as RouterLink } from 'react-router-dom';
import { PageContainer, SectionCard } from '../components/Layout';

function Home() {
  return (
    <PageContainer>
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h3" component="h1" sx={{ fontWeight: 800 }}>
          HATVP Explorer
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" sx={{ mt: 1 }}>
          Explore transparency data from French public officials — organizations mentioned,
          demographics, and declaration timelines.
        </Typography>
      </Box>

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <SectionCard>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <InsightsIcon color="primary" />
              <Typography variant="h6">Top Organization Mentions</Typography>
            </Box>
            <Typography variant="body2" color="text.secondary">
              See which organizations are most frequently referenced across declarations.
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Button component={RouterLink} to="/organizations" variant="contained">
                Explore organizations
              </Button>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={6}>
          <SectionCard>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <PeopleIcon color="primary" />
              <Typography variant="h6">Demographics</Typography>
            </Box>
            <Typography variant="body2" color="text.secondary">
              Explore distributions by role, gender, and other attributes.
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Button component={RouterLink} to="/demographics" variant="outlined">
                View demographics
              </Button>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={6}>
          <SectionCard>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <ScheduleIcon color="primary" />
              <Typography variant="h6">Declaration Delays</Typography>
            </Box>
            <Typography variant="body2" color="text.secondary">
              Analyze timing and potential delays in submissions by mandate.
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Button component={RouterLink} to="/delay" variant="outlined">
                Analyze delays
              </Button>
            </Box>
          </SectionCard>
        </Grid>

        <Grid item xs={12} md={6}>
          <SectionCard>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <InfoIcon color="primary" />
              <Typography variant="h6">About</Typography>
            </Box>
            <Typography variant="body2" color="text.secondary">
              Learn about data sources, ethics, and methodology.
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Button component={RouterLink} to="/about" variant="text">
                Read more
              </Button>
            </Box>
          </SectionCard>
        </Grid>
      </Grid>
    </PageContainer>
  );
}

export default Home;

