import * as React from 'react';
import PropTypes from 'prop-types';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Divider from '@mui/material/Divider';
import Chip from '@mui/material/Chip';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Tooltip from '@mui/material/Tooltip';

import InfoIcon from '@mui/icons-material/Info';
import InsightsIcon from '@mui/icons-material/Insights';
import SecurityIcon from '@mui/icons-material/Security';
import PublicIcon from '@mui/icons-material/Public';
import GitHubIcon from '@mui/icons-material/GitHub';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import ArticleIcon from '@mui/icons-material/Article';
import BugReportIcon from '@mui/icons-material/BugReport';
import AlternateEmailIcon from '@mui/icons-material/AlternateEmail';
import SpeedIcon from '@mui/icons-material/Speed';
import DataObjectIcon from '@mui/icons-material/DataObject';
import GavelIcon from '@mui/icons-material/Gavel';
import TimelineIcon from '@mui/icons-material/Timeline';
import DownloadIcon from '@mui/icons-material/Download';

/**
 * JSX-safe About page (no TypeScript syntax).
 * If you prefer TS, rename to About.tsx and add the types back.
 */

export default function About({
  version = 'v0.1.0',
  lastUpdated = '2025-08-10',
  stats = { declarants: 2607, documents: 526, equities: 2050000000 },
  repoUrl = 'https://github.com/your-org/hatvp-explorer',
  dataLicenseUrl = 'https://creativecommons.org/licenses/by/4.0/',
  contactEmail = 'contact@example.org',
}) {
  const formatter = new Intl.NumberFormat();
  const euros = new Intl.NumberFormat(undefined, { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });

  return (
    <Container maxWidth="lg" sx={{ py: { xs: 4, md: 6 } }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
        <InfoIcon color="primary" fontSize="large" />
        <Typography variant="h3" component="h1" sx={{ fontWeight: 700 }}>
          HATVP Explorer
        </Typography>
        <Chip label={version} size="small" sx={{ ml: 1 }} />
      </Box>
      <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 3 }}>
        Analyses des déclarations publiques pour cartographier intérêts financiers, mandats et zones de risque.
      </Typography>

      {/* Quick links / TOC */}
      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 4 }}>
        <Chip clickable component="a" href="#purpose" label="Purpose" variant="outlined" />
        <Chip clickable component="a" href="#sources" label="Data & Methods" variant="outlined" />
        <Chip clickable component="a" href="#results" label="Key Insights" variant="outlined" />
        <Chip clickable component="a" href="#limits" label="Limitations" variant="outlined" />
        <Chip clickable component="a" href="#faq" label="FAQ" variant="outlined" />
        <Chip clickable component="a" href="#contribute" label="Contribute" variant="outlined" />
      </Stack>

      {/* Intro / Purpose */}
      <Grid container spacing={3} id="purpose" sx={{ scrollMarginTop: 96 }}>
        <Grid item xs={12} md={7}>
          <Paper variant="outlined" sx={{ p: 3 }}>
            <Stack spacing={2}>
              <Stack direction="row" spacing={1} alignItems="center">
                <InsightsIcon color="primary" />
                <Typography variant="h5" component="h2" sx={{ fontWeight: 700 }}>
                  What is this?
                </Typography>
              </Stack>

              <Typography>
                <span role="img" aria-label="sparkles">✨</span>{' '}HATVP Explorer presents analyses based on public data from the{' '}
                <Link href="https://www.hatvp.fr/" target="_blank" rel="noopener">Haute Autorité pour la transparence de la vie publique</Link>.
                It helps journalists, researchers, and citizens quickly understand potential{' '}
                conflicts of interest, patterns in asset holdings, and the network of mandates.
              </Typography>

              <Alert severity="info" icon={<PublicIcon />}>
                Last updated: <strong>{lastUpdated}</strong>. Data is refreshed periodically; see the FAQ for cadence.
              </Alert>
            </Stack>
          </Paper>
        </Grid>

        {/* Key Figures */}
        <Grid item xs={12} md={5}>
          <Stack spacing={2}>
            <StatCard icon={<TimelineIcon />} label="Declarants" value={formatter.format((stats && stats.declarants) || 0)} />
            <StatCard icon={<ArticleIcon />} label="Documents processed" value={formatter.format((stats && stats.documents) || 0)} />
            <StatCard icon={<SpeedIcon />} label="Total declared equities" value={euros.format((stats && stats.equities) || 0)} />
          </Stack>
        </Grid>
      </Grid>

      {/* Methods & sources */}
      <Box id="sources" sx={{ scrollMarginTop: 96, mt: 4 }}>
        <SectionTitle icon={<DataObjectIcon color="primary" />} title="Data Sources & Methodology" />
        <Paper variant="outlined" sx={{ p: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>Sources</Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon><ArticleIcon /></ListItemIcon>
                  <ListItemText
                    primary={
                      <span>
                        HATVP deliberations & decisions — OCRed PDFs and structured XML exports.
                      </span>
                    }
                    secondary={
                      <span>
                        Licensed under <Link href={dataLicenseUrl} target="_blank" rel="noopener">CC BY 4.0</Link> where applicable.
                      </span>
                    }
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon><OpenInNewIcon /></ListItemIcon>
                  <ListItemText primary="Issuer & index membership (CAC40/SBF120/SP500) for context" secondary="Used to normalize issuer names and benchmark exposure." />
                </ListItem>
              </List>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>Pipeline (high‑level)</Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon><DataObjectIcon /></ListItemIcon>
                  <ListItemText primary="Parse & normalize" secondary="Clean names, dedupe entities, standardize units & currencies." />
                </ListItem>
                <ListItem>
                  <ListItemIcon><InsightsIcon /></ListItemIcon>
                  <ListItemText primary="Extract & enrich" secondary="NER on people/orgs; enrich with index membership & sector tags." />
                </ListItem>
                <ListItem>
                  <ListItemIcon><TimelineIcon /></ListItemIcon>
                  <ListItemText primary="Analyze & flag" secondary="Aggregate positions, surface outliers, and map mandate overlaps." />
                </ListItem>
              </List>
            </Grid>
          </Grid>
        </Paper>
      </Box>

      {/* Results blurb */}
      <Box id="results" sx={{ scrollMarginTop: 96, mt: 4 }}>
        <SectionTitle icon={<InsightsIcon color="primary" />} title="What we surface" />
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <FeatureCard title="Holdings & Exposure" icon={<TimelineIcon />}>
              Trends across thousands of records; concentration by issuer and sector; significant stakes worth extra scrutiny.
            </FeatureCard>
          </Grid>
          <Grid item xs={12} md={4}>
            <FeatureCard title="Mandates & Roles" icon={<GavelIcon />}>
              Elected/appointed positions and overlaps that may create perceived or real conflicts of interest.
            </FeatureCard>
          </Grid>
          <Grid item xs={12} md={4}>
            <FeatureCard title="Entity Graph" icon={<SecurityIcon />}>
              Cleaned people/org entities suitable for network analysis and newsroom workflows.
            </FeatureCard>
          </Grid>
        </Grid>
      </Box>

      {/* Limitations */}
      <Box id="limits" sx={{ scrollMarginTop: 96, mt: 4 }}>
        <SectionTitle icon={<SecurityIcon color="primary" />} title="Limitations & Responsible Use" />
        <Alert severity="warning" sx={{ mb: 2 }}>
          This explorer aggregates public records and may contain OCR or parsing errors. Findings are <strong>leads</strong>, not conclusions.
          Always corroborate with primary sources.
        </Alert>
        <Paper variant="outlined" sx={{ p: 3 }}>
          <List dense>
            <ListItem>
              <ListItemIcon><BugReportIcon /></ListItemIcon>
              <ListItemText primary="Data quality" secondary="OCR may misread names/amounts; entity resolution is probabilistic." />
            </ListItem>
            <ListItem>
              <ListItemIcon><ArticleIcon /></ListItemIcon>
              <ListItemText primary="Context matters" secondary="Declared holdings do not imply wrongdoing; they inform risk assessment." />
            </ListItem>
            <ListItem>
              <ListItemIcon><SecurityIcon /></ListItemIcon>
              <ListItemText primary="Privacy & ethics" secondary="Only public-interest signals are highlighted; no personal data beyond official records." />
            </ListItem>
          </List>
        </Paper>
      </Box>

      {/* FAQ */}
      <Box id="faq" sx={{ scrollMarginTop: 96, mt: 4 }}>
        <SectionTitle icon={<InfoIcon color="primary" />} title="FAQ" />
        <Accordion defaultExpanded>
          <AccordionSummary expandIcon={<OpenInNewIcon />}>How often is the data refreshed?</AccordionSummary>
          <AccordionDetails>
            We target periodic refreshes; check the version badge and changelog in the repository for exact cadence.
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary expandIcon={<OpenInNewIcon />}>Can I download the cleaned datasets?</AccordionSummary>
          <AccordionDetails>
            Yes. Use the download buttons across the app or fetch CSV/JSON artifacts from the releases page.
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary expandIcon={<OpenInNewIcon />}>Is this an official HATVP product?</AccordionSummary>
          <AccordionDetails>
            No. This is an independent analysis project relying on public HATVP materials.
          </AccordionDetails>
        </Accordion>
      </Box>

      {/* Contribute / CTA */}
      <Box id="contribute" sx={{ scrollMarginTop: 96, mt: 4 }}>
        <SectionTitle icon={<GitHubIcon color="primary" />} title="Contribute & Contact" />
        <Paper variant="outlined" sx={{ p: 3 }}>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems={{ xs: 'stretch', sm: 'center' }}>
            <Tooltip title="Open repository">
              <Button variant="contained" startIcon={<GitHubIcon />} href={repoUrl} target="_blank" rel="noopener">
                View on GitHub
              </Button>
            </Tooltip>
            <Tooltip title="Report a parsing or data issue">
              <Button variant="outlined" startIcon={<BugReportIcon />} href={`${repoUrl}/issues`} target="_blank" rel="noopener">
                Report an issue
              </Button>
            </Tooltip>
            <Tooltip title="Download latest release data">
              <Button variant="text" startIcon={<DownloadIcon />} href={`${repoUrl}/releases`} target="_blank" rel="noopener">
                Download data
              </Button>
            </Tooltip>
            <Box sx={{ flex: 1 }} />
            <Button variant="text" startIcon={<AlternateEmailIcon />} href={`mailto:${contactEmail}`}>
              {contactEmail}
            </Button>
          </Stack>
        </Paper>
      </Box>

      <Divider sx={{ my: 4 }} />

      {/* Footer note */}
      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} alignItems={{ xs: 'flex-start', sm: 'center' }} sx={{ color: 'text.secondary' }}>
        <Typography variant="body2">
          Built for investigative workflows and civic oversight. Data where applicable under{' '}
          <Link href={dataLicenseUrl} target="_blank" rel="noopener">CC BY 4.0</Link>.
        </Typography>
        <Box sx={{ display: { xs: 'none', sm: 'inline' } }}>•</Box>
        <Typography variant="body2">Version {version} • Updated {lastUpdated}</Typography>
      </Stack>
    </Container>
  );
}

About.propTypes = {
  version: PropTypes.string,
  lastUpdated: PropTypes.string,
  stats: PropTypes.shape({
    declarants: PropTypes.number,
    documents: PropTypes.number,
    equities: PropTypes.number,
  }),
  repoUrl: PropTypes.string,
  dataLicenseUrl: PropTypes.string,
  contactEmail: PropTypes.string,
};

function SectionTitle({ icon, title }) {
  return (
    <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
      {icon}
      <Typography variant="h5" component="h2" sx={{ fontWeight: 700 }}>{title}</Typography>
    </Stack>
  );
}

function StatCard({ icon, label, value }) {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Stack direction="row" spacing={2} alignItems="center">
        <Box aria-hidden>{icon}</Box>
        <Box>
          <Typography variant="overline" color="text.secondary">{label}</Typography>
          <Typography variant="h6" sx={{ fontWeight: 700 }}>{value}</Typography>
        </Box>
      </Stack>
    </Paper>
  );
}

function FeatureCard({ title, icon, children }) {
  return (
    <Paper variant="outlined" sx={{ p: 3, height: '100%' }}>
      <Stack spacing={1}>
        <Stack direction="row" spacing={1} alignItems="center">
          <Box aria-hidden>{icon}</Box>
          <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>{title}</Typography>
        </Stack>
        <Typography variant="body2" color="text.secondary">
          {children}
        </Typography>
      </Stack>
    </Paper>
  );
}
