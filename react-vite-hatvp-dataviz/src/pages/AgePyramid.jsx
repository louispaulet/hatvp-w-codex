import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';

function AgePyramid() {
  const [data, setData] = useState([]);

  useEffect(() => {
    d3.csv('/age_pyramid.csv', d => ({
      age_band: d.age_band,
      male: +d.male,
      female: +d.female,
    })).then(raw => {
      raw.sort((a, b) => {
        const ageA = parseInt(a.age_band.split('-')[0], 10);
        const ageB = parseInt(b.age_band.split('-')[0], 10);
        return ageB - ageA; // Oldest first
      });
      setData(raw);
    });
  }, []);

  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom>
        Age Pyramid by Gender
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Age distribution split by gender.
      </Typography>
      <Paper sx={{ mt: 3 }}>
        <Box sx={{ height: { xs: 500, md: 700 }, maxWidth: 900, mx: 'auto' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} layout="vertical" stackOffset="sign">
              <XAxis type="number" domain={['dataMin', 'dataMax']} />
              <YAxis dataKey="age_band" type="category" />
              <Tooltip formatter={(value) => Math.abs(value)} />
              <Bar dataKey="male" stackId="a" fill="#1976d2" name="Male" />
              <Bar dataKey="female" stackId="a" fill="#ef4444" name="Female" />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </Paper>
    </Container>
  );
}

export default AgePyramid;
