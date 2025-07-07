# ShikshaSetu - Indian Scholarship Portal

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview

ShikshaSetu is a production-grade Indian scholarship portal that scrapes live data from trusted sources and provides authentic scholarship opportunities to students.

## Architecture Guidelines

- **Frontend**: Next.js 14 with App Router, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI with Python for scraping and API services
- **Database**: PostgreSQL with Prisma ORM
- **Scraping**: Playwright + LangChain for AI-powered extraction
- **Background Jobs**: Celery + Redis
- **Containerization**: Docker with multi-service deployment

## Code Standards

- Use TypeScript for all frontend code
- Follow Next.js 14 App Router patterns
- Use Tailwind CSS for styling with shadcn/ui components
- Implement proper error handling and validation
- Use React Query/SWR for data fetching
- Follow accessibility guidelines (WCAG 2.1 AA)
- Implement mobile-first responsive design

## Key Features to Implement

- Real-time scholarship scraping from trusted Indian sources
- Link validation and quality scoring
- Admin dashboard for monitoring
- Student portal with search and filters
- Authentication and user management
- Background job processing
- Comprehensive monitoring and logging

## Security Considerations

- Implement JWT authentication
- Validate all user inputs
- Use environment variables for sensitive data
- Implement rate limiting
- Follow OWASP security guidelines

## Performance Guidelines

- Implement caching strategies
- Use lazy loading for components
- Optimize database queries
- Implement proper error boundaries
- Use background workers for heavy tasks
