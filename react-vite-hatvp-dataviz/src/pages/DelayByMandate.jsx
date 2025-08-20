import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import TimelineIcon from '@mui/icons-material/Timeline';
import { PageContainer, SectionCard } from '../components/Layout';
import SectionTitle from '../components/SectionTitle';
import Box from '@mui/material/Box';
import HomeButton from '../components/HomeButton';

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
      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
        <HomeButton variant="outlined" />
      </Box>
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
      <SectionCard sx={{ mt: 2 }}>
        <SectionTitle icon={<TimelineIcon color="primary" />} title="About this chart" />
        <div style={{ marginTop: 8 }}>
          <Typography variant="subtitle2">Description of the chart</Typography>
          <ul style={{ marginTop: 4, marginBottom: 8 }}>
            <li>
              <Typography variant="body2">
                This bar chart shows the <strong>median delay (in days) between deposit and publication</strong> of HATVP declarations, split by type of mandate.
              </Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>x-axis</strong>: type of mandate (Europe, deputy, commune, EPCI, département, region, CTSP, senator, government, president, other).</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>y-axis</strong>: median number of days (up to just over 300).</Typography>
            </li>
          </ul>
          <Divider sx={{ my: 1.5 }} />
          <Typography variant="subtitle2">Key observations</Typography>
          <ul style={{ marginTop: 4 }}>
            <li>
              <Typography variant="body2"><strong>Longest delays</strong>: <strong>Europe (~320 days)</strong> and <strong>deputies (~280 days)</strong> have the slowest publication times.</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Medium delays (200–250 days)</strong>: Communes, EPCIs, départements, regions, CTSP → around <strong>200 days</strong>.</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Shorter delays (100–200 days)</strong>: Senators: about <strong>170 days</strong>.</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Fastest publication</strong>: Government (~100 days), President (~80 days), Other (~75 days).</Typography>
            </li>
          </ul>
          <Divider sx={{ my: 1.5 }} />
          <Typography variant="subtitle2">Analysis</Typography>
          <Typography variant="body2" sx={{ mt: 0.5 }}>
            There is a kind of <strong>inverse hierarchy</strong>: the higher the political level (President, Government), the <strong>faster</strong> the declaration is published. Local mandates and deputies face <strong>longer delays</strong>, likely due to heavier administrative workload, a larger number of declarations to process, and less direct political/media pressure for quick transparency.
          </Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            <strong>European mandates stand out</strong> with the longest delays — probably due to additional layers of procedure at the supranational level.
          </Typography>
          <Typography variant="subtitle2" sx={{ mt: 1.5 }}>In summary</Typography>
          <ul style={{ marginTop: 4 }}>
            <li>
              <Typography variant="body2"><strong>President & Government</strong> → fast publication (high political/media pressure).</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Deputies & Europe</strong> → very slow publication (more than 9 months delay).</Typography>
            </li>
            <li>
              <Typography variant="body2"><strong>Local & regional mandates</strong> → medium delay (6–8 months).</Typography>
            </li>
          </ul>
          
        </div>
      </SectionCard>
    </PageContainer>
  );
}

export default DelayByMandate;
