import { render, screen } from "@testing-library/react";

jest.mock("./api", () => ({
  __esModule: true,
  fetchBootstrap: jest.fn(() =>
    Promise.resolve({
      education_levels: ["After 10th", "After 12th", "Graduation"],
    })
  ),
  analyzeStudent: jest.fn(),
  toggleRoadmapStep: jest.fn(),
  saveSubjectProgress: jest.fn(),
  refreshStudyPlan: jest.fn(),
}));

const App = require("./App").default;

test("renders EduPath AI hero text", async () => {
  render(<App />);
  expect(await screen.findByText(/career clarity for students/i)).toBeInTheDocument();
});
