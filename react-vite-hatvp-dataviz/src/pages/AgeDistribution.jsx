import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Typography from '@mui/material/Typography';
import InsightsIcon from '@mui/icons-material/Insights';
import { PageContainer, SectionCard } from '../components/Layout';
import SectionTitle from '../components/SectionTitle';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';

function AgeDistribution() {
  const [data, setData] = useState([]);

  useEffect(() => {
    d3.csv('/age_band_counts.csv', d => ({
      age_band: d.age_band,
      count: +d.count,
    })).then(setData);
  }, []);

  return (
    <PageContainer>
      <SectionTitle icon={<InsightsIcon color="primary" />} title="Declarant Age Distribution" subtitle="Age bands among declarants." />
      <SectionCard sx={{ mt: 2, height: 420 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="age_band" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#1976d2" />
          </BarChart>
        </ResponsiveContainer>
      </SectionCard>
      <SectionCard sx={{ mt: 2 }}>
        <SectionTitle icon={<InsightsIcon color="primary" />} title="About this chart" />
        <Box sx={{ mt: 1 }}>
          <Typography variant="body1" sx={{ mb: 1 }}>
            This bar chart shows the <strong>age distribution of declarants</strong> across different age bands.
          </Typography>
          <Typography variant="subtitle2" sx={{ mt: 1 }}>What it shows</Typography>
          <ul style={{ marginTop: 4, marginBottom: 8 }}>
            <li>
              <Typography variant="body2">
                The <strong>x-axis</strong> represents age groups in 10-year bands (20–29, 30–39, …, 90–99).
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                The <strong>y-axis</strong> represents the number of declarants, ranging from 0 to about 3800.
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                The <strong>bars</strong> represent how many declarants fall within each age group.
              </Typography>
            </li>
          </ul>
          <Divider sx={{ my: 1.5 }} />
          <Typography variant="subtitle2">Key observations</Typography>
          <ul style={{ marginTop: 4 }}>
            <li>
              <Typography variant="body2">The distribution is <strong>centered around middle-aged groups</strong>.</Typography>
            </li>
            <li>
              <Typography variant="body2">
                The <strong>50–59</strong> age group has the highest count (~3800), followed closely by <strong>60–69</strong> (~3300).
              </Typography>
            </li>
            <li>
              <Typography variant="body2">The <strong>40–49</strong> age group also has a high number (~2300).</Typography>
            </li>
            <li>
              <Typography variant="body2">Very few declarants are below 30 or above 80.</Typography>
            </li>
            <li>
              <Typography variant="body2">
                The counts drop significantly for <strong>70–79</strong>, and are almost negligible for <strong>80–89</strong> and <strong>90–99</strong>.
              </Typography>
            </li>
          </ul>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Overall, most declarants are between <strong>40 and 69 years old</strong>, with a clear peak in the <strong>50–59</strong> range.
          </Typography>
        </Box>
      </SectionCard>
    </PageContainer>
  );
}

export default AgeDistribution;
