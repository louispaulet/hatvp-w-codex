import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import InfoIcon from '@mui/icons-material/Info';
import EmojiObjectsIcon from '@mui/icons-material/EmojiObjects';

function About() {
  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Box display="flex" alignItems="center" mb={2}>
        <InfoIcon color="primary" sx={{ mr: 1 }} />
        <Typography variant="h4" component="h1" gutterBottom>
          About HATVP Explorer
        </Typography>
      </Box>
      <Typography variant="body1" paragraph>
        <span role="img" aria-label="sparkles">✨</span> HATVP Explorer presents analyses from the{' '}
        <Link href="https://www.hatvp.fr/" target="_blank" rel="noopener">
          Haute Autorité pour la transparence de la vie publique
        </Link>
        , France's authority for public-sector transparency.
      </Typography>
      <Typography variant="body1" paragraph>
        <span role="img" aria-label="chart">📊</span> We process asset declarations to map financial interests, mandates, and potential conflicts.
        Current results highlight trends across thousands of documents and surface noteworthy stock positions.
      </Typography>
      <Typography variant="body1" paragraph>
        <span role="img" aria-label="handshake">🤝</span> Built for investigative journalists and engaged citizens, these tools help foster trust through open data.
      </Typography>
      <Typography variant="body1" paragraph sx={{ display: 'flex', alignItems: 'center' }}>
        <EmojiObjectsIcon color="secondary" sx={{ mr: 1 }} />
        Explore the visualizations, share insights, and contribute to a more transparent democracy.
      </Typography>
    </Container>
  );
}

export default About;
