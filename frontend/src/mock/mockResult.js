export const mockResult = {
  skills: ["Python", "SQL", "Git", "Pandas"],
  careers: [
    { id: "data-analyst", name: "Data Analyst", score: 0.85 },
    { id: "data-scientist", name: "Data Scientist", score: 0.72 },
    { id: "backend-developer", name: "Backend Developer", score: 0.55 },
  ],
  skill_gap: [
    { skill: "Power BI", priority: "high" },
    { skill: "Statistics", priority: "medium" },
    { skill: "Docker", priority: "low" },
  ],
  roadmap: [
    {
      step: 1,
      skill: "Power BI",
      priority: "high",
      duration_weeks: 3,
      resources: [
        { title: "Power BI documentation", url: "https://learn.microsoft.com/power-bi/" },
      ],
    },
    {
      step: 2,
      skill: "Statistics",
      priority: "medium",
      duration_weeks: 4,
      resources: [
        { title: "Khan Academy: Statistics", url: "https://www.khanacademy.org/math/statistics-probability" },
      ],
    },
    {
      step: 3,
      skill: "Docker",
      priority: "low",
      duration_weeks: 2,
      resources: [
        { title: "Docker: Get started", url: "https://docs.docker.com/get-started/" },
      ],
    },
  ],
};