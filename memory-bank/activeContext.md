# SimpleMediaSocial Active Context

## Current Work Focus
- Implementing post reply functionality
- Maintaining engagement counts
- Tracking post modification timestamps

## Recent Changes
- Added reply functionality to posts
- Implemented updated_at and modified_at timestamps
- Removed counts from posts endpoint response
- Fixed func import in interactions router
- Added proper schema definitions

## Next Steps
1. Test reply functionality
2. Verify timestamp updates
3. Review API response formats
4. Document new endpoints

## Active Decisions
- Using SQLite for development simplicity
- JWT for authentication
- Repository pattern for data access
- Tracking both content and general updates

## Important Patterns
- Follow RESTful conventions
- Keep endpoints focused and simple
- Use dependency injection for services
- Parent-child relationship for post replies
- Separate timestamps for content vs general updates
