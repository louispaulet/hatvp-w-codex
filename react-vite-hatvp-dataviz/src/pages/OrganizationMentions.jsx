import { useEffect, useMemo, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import InputAdornment from '@mui/material/InputAdornment';
import SearchIcon from '@mui/icons-material/Search';
import InsightsIcon from '@mui/icons-material/Insights';
import { PageContainer, SectionCard } from '../components/Layout';
import HomeButton from '../components/HomeButton';
import SectionTitle from '../components/SectionTitle';

function OrganizationMentions() {
  const [allData, setAllData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [topN, setTopN] = useState(10);

  useEffect(() => {
    d3.csv('/organization_mentions.csv', d => ({
      organization: d.organization,
      mentions: +d.mentions,
    })).then(csvData => {
      const filtered = csvData.filter(d => d.mentions > 0);
      setAllData(filtered);
    });
  }, []);

  const data = useMemo(() => {
    return allData
      .filter(d =>
        d.organization.toLowerCase().includes(searchTerm.toLowerCase()),
      )
      .sort((a, b) => b.mentions - a.mentions)
      .slice(0, topN);
  }, [allData, searchTerm, topN]);

  return (
    <PageContainer>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
        <HomeButton variant="outlined" />
      </Box>
      <SectionTitle icon={<InsightsIcon color="primary" />} title="Top Organization Mentions" subtitle="Explore which organizations are most frequently referenced in declarations." />
      <Box sx={{ mt: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={8} md={6}>
            <TextField
              fullWidth
              id="search"
              label="Search"
              variant="outlined"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Type a name..."
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon color="action" />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} sm={4} md={3}>
            <TextField
              fullWidth
              id="topn"
              label="Top N"
              type="number"
              inputProps={{ min: 1, max: 50 }}
              value={topN}
              onChange={(e) => setTopN(Math.max(1, Number(e.target.value)))}
            />
          </Grid>
        </Grid>
      </Box>
      <SectionCard sx={{ mt: 2, height: 420 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="organization" angle={-45} textAnchor="end" height={120} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="mentions" fill="#1976d2" />
          </BarChart>
        </ResponsiveContainer>
      </SectionCard>
      <SectionCard sx={{ mt: 2 }}>
        <SectionTitle icon={<InsightsIcon color="primary" />} title="About this chart" />
        <div style={{ marginTop: 8 }}>
          <Typography variant="subtitle2">Description of the chart</Typography>
          <ul style={{ marginTop: 4, marginBottom: 8 }}>
            <li>
              <Typography variant="body2">
                The bar chart shows the <strong>most frequently mentioned organizations</strong> in HATVP declarations, specifically in the context of ethics-related debates.
              </Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>x-axis</strong>: organization names.</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>y-axis</strong>: frequency of mentions (up to ~50).</Typography>
            </li>
          </ul>
          <Divider sx={{ my: 1.5 }} />
          <Typography variant="subtitle2">Key observations</Typography>
          <ul style={{ marginTop: 4 }}>
            <li>
              <Typography variant="body2"><strong>Most cited organizations</strong>: <strong>Pasteur (~46)</strong> leads. <strong>Commissariat (~32)</strong> and <strong>Renaissance (~31)</strong> follow closely.</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Second tier</strong>: <strong>Horizons (~18 mentions)</strong>.</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Occasional mentions</strong>: <strong>Assistance Publique</strong>, <strong>Edenred</strong>, <strong>Stellantis</strong>, <strong>Enedis</strong>, <strong>Soreqa</strong>, and <strong>Retailleau</strong> each have fewer than ~10 mentions.</Typography>
            </li>
          </ul>
          <Divider sx={{ my: 1.5 }} />
          <Typography variant="subtitle2">Analysis</Typography>
          <Typography variant="body2" sx={{ mt: 0.5 }}>
            The dominance of <strong>Pasteur</strong> suggests frequent declarations involving research, public health, or bioethics connections. <strong>Commissariat</strong> and <strong>Renaissance</strong> (a political party) highlight institutional and political overlaps in ethics discussions. The presence of <strong>Horizons</strong> (another political party) further shows that <strong>political affiliations are a recurring theme</strong> in declarations.
          </Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            Companies such as <strong>Edenred</strong> (payments), <strong>Stellantis</strong> (automotive), and <strong>Enedis</strong> (energy) show that <strong>corporate ties</strong> also appear in declarations, though less frequently. The mix of <strong>public health, politics, and private corporations</strong> suggests that ethical concerns in declarations often arise at the intersection of <strong>public service, political life, and industry links</strong>.
          </Typography>
          <Typography variant="subtitle2" sx={{ mt: 1.5 }}>In short</Typography>
          <ul style={{ marginTop: 4 }}>
            <li>
              <Typography variant="body2"><strong>Pasteur & health sector</strong> → top mentions (bioethics, medical ties).</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Political parties (Renaissance, Horizons)</strong> → strong presence (conflicts of interest in politics).</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Corporates (Stellantis, Edenred, Enedis)</strong> → less frequent, but relevant in lobbying/ethics debates.</Typography>
            </li>
          </ul>
          
        </div>
      </SectionCard>
    </PageContainer>
  );
}

export default OrganizationMentions;
