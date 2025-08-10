import { useEffect, useMemo, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import InputAdornment from '@mui/material/InputAdornment';
import SearchIcon from '@mui/icons-material/Search';

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
    <Container>
      <Typography variant="h4" component="h1" gutterBottom>
        Top Organization Mentions
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Explore which organizations are most frequently referenced in declarations.
      </Typography>
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
      <Paper sx={{ mt: 3, height: 420 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="organization" angle={-45} textAnchor="end" height={120} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="mentions" fill="#1976d2" />
          </BarChart>
        </ResponsiveContainer>
      </Paper>
    </Container>
  );
}

export default OrganizationMentions;
