import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Typography from '@mui/material/Typography';
import TimelineIcon from '@mui/icons-material/Timeline';
import { PageContainer, SectionCard } from '../components/Layout';
import SectionTitle from '../components/SectionTitle';

function DelayByMandate() {
  const [data, setData] = useState([]);

  useEffect(() => {
    d3.csv('/mandate_delay_median.csv', d => ({
      mandate_type: d.mandate_type,
      delay_days: +d.delay_days,
    })).then(setData);
  }, []);

  return (
    <PageContainer>
      <SectionTitle icon={<TimelineIcon color="primary" />} title="Median Publication Delay by Mandate" subtitle="Median days between deposit and publication." />
      <SectionCard sx={{ mt: 2, height: 420 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="mandate_type" angle={-45} textAnchor="end" height={120} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="delay_days" fill="#1976d2" />
          </BarChart>
        </ResponsiveContainer>
      </SectionCard>
    </PageContainer>
  );
}

export default DelayByMandate;
