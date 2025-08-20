import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import StackedBarChartIcon from '@mui/icons-material/StackedBarChart';
import { SectionCard } from '../Layout';
import SectionTitle from '../SectionTitle';

function AgePyramidSection() {
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
    <>
      <SectionCard sx={{ mt: 2 }}>
        <SectionTitle icon={<StackedBarChartIcon color="primary" />} title="Age Pyramid by Gender" />
        <Box sx={{ height: { xs: 500, md: 700 }, maxWidth: 900, mx: 'auto', mt: 2 }}>
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
        <Divider variant="middle" sx={{ my: 2 }} />
        <Box sx={{ mt: 1 }}>
          <Typography variant="body1" sx={{ mb: 1 }}>
            This is an <strong>age pyramid by gender</strong> of HATVP declarants (people declaring assets/interests).
          </Typography>
          <Typography variant="subtitle2" sx={{ mt: 1 }}>What it shows</Typography>
          <ul style={{ marginTop: 4, marginBottom: 8 }}>
            <li>
              <Typography variant="body2">
                The <strong>y-axis</strong> shows age groups in 10-year bands (20–29 up to 90–99).
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                The <strong>x-axis</strong> shows the number of declarants, with <strong>men in blue</strong> (left, negative values) and <strong>women in red</strong> (right, positive values).
              </Typography>
            </li>
          </ul>
          <Divider sx={{ my: 1.5 }} />
          <Typography variant="subtitle2">Key observations</Typography>
          <ul style={{ marginTop: 4 }}>
            <li>
              <Typography variant="body2"><strong>Middle-aged dominance</strong>: Most declarants are between <strong>40–69 years old</strong>, with peaks at <strong>50–59</strong> and <strong>60–69</strong>.</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Gender imbalance</strong>: Men heavily dominate almost every age group, especially <strong>40–69</strong>; the gap is smaller but still male‑leaning in <strong>50–59</strong>. Younger (20–39) and older (70–89) groups also skew male.</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Extremes</strong>: Few declarants under 30 or over 80, and those who exist are still mostly men.</Typography>
            </li>
          </ul>
          <Divider sx={{ my: 1.5 }} />
          <Typography variant="subtitle2">Analysis</Typography>
          <Typography variant="body2" sx={{ mt: 0.5 }}>
            The pyramid reveals a <strong>structural gender imbalance</strong> among HATVP declarants, reflecting a broader <strong>gender disparity in political and public office representation</strong> in France. The overrepresentation of men in the <strong>40–69</strong> bands suggests that decision‑making cohorts remain largely male. Women are present but never match men’s counts, indicating the <strong>pipeline to positions requiring HATVP declarations remains unequal</strong>.
          </Typography>
          <Typography variant="subtitle2" sx={{ mt: 1.5 }}>In short</Typography>
          <ul style={{ marginTop: 4 }}>
            <li>
              <Typography variant="body2"><strong>Age trend</strong>: Concentrated in mid‑to‑late career (40–69).</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Gender trend</strong>: Strong male dominance, highlighting an ongoing gap in access to public roles.</Typography>
            </li>
          </ul>
        </Box>
      </SectionCard>
    </>
  );
}

export default AgePyramidSection;
