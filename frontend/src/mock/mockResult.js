export const mockResult = {
  skills: ["Python", "SQL", "Git", "Pandas"],
  careers: [
    {
      career_id: "data-analyst",
      career_name: "Data Analyst",
      score: 0.85,
      matched_skills: ["Python", "SQL"],
      missing_skills: ["Power BI", "Statistics"],
    },
    {
      career_id: "backend-developer",
      career_name: "Backend Developer",
      score: 0.55,
      matched_skills: ["Python", "Git"],
      missing_skills: ["Django", "Docker"],
    },
  ],
  skill_gap: [
    {
      career_id: "data-analyst",
      career_name: "Data Analyst",
      gap_count: 2,
      missing_skills: ["Power BI", "Statistics"],
      priority: "medium",
    },
    {
      career_id: "backend-developer",
      career_name: "Backend Developer",
      gap_count: 2,
      missing_skills: ["Django", "Docker"],
      priority: "high",
    },
  ],
  roadmap: [
    {
      career_id: "data-analyst",
      career_name: "Data Analyst",
      steps: [
        { skill: "Power BI", tasks: ["Learn the basics", "Build a sales dashboard"] },
        { skill: "Statistics", tasks: ["Review descriptive statistics", "Practice hypothesis testing"] },
      ],
    },
    {
      career_id: "backend-developer",
      career_name: "Backend Developer",
      steps: [],
    },
  ],
};