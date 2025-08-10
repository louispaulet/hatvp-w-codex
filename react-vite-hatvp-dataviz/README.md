# HATVP Organization Mentions Visualizations

Interactive visualizations of organization mentions from HATVP datasets.

## Dataset

The app reads `public/organization_mentions.csv`, which lists how often each organization is mentioned across declarations. The main view displays a bar chart of the top organizations sorted by mention count, with organization names on the y-axis and counts on the x-axis.

## Dependencies

- [d3](https://d3js.org/) for parsing CSV data
- [Recharts](https://recharts.org/) for rendering the bar chart
- [Tailwind CSS](https://tailwindcss.com/) for styling

## Development

Install dependencies and start the dev server:

```bash
npm install
npm run dev
```

Build the app for production:

```bash
npm run build
```
