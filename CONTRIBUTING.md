# Contributing to AI Vision Agent Pro

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/ai-vision-agent-pro/issues)
2. If not, create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, Docker version, etc.)

### Suggesting Features

1. Open an issue with tag `enhancement`
2. Describe the feature and its use case
3. Explain why it would benefit users

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest
   
   # Frontend tests
   cd frontend
   npm test
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Amazing new feature"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/amazing-feature
   ```

## Development Guidelines

### Code Style

**Python (Backend)**
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Keep functions focused and small

**JavaScript (Frontend)**
- Use ES6+ features
- Use functional components
- Keep components under 300 lines
- Use meaningful variable names

### Commit Messages

Format: `Type: Brief description`

Types:
- `Add`: New feature
- `Fix`: Bug fix
- `Update`: Changes to existing feature
- `Refactor`: Code restructuring
- `Docs`: Documentation changes
- `Style`: Code formatting
- `Test`: Adding tests

Examples:
```
Add: WebSocket support for real-time updates
Fix: CORS error on production deployment
Update: Improve prompt optimization algorithm
Docs: Add API endpoint examples
```

### Testing

- Write tests for new features
- Ensure all tests pass before PR
- Maintain >80% code coverage

### Documentation

- Update README.md for new features
- Add inline comments for complex code
- Update API documentation in code

## Project Structure

```
backend/
  app/
    api/        # REST endpoints
    agent/      # LangGraph logic
    services/   # External integrations

frontend/
  src/
    components/ # React components
    hooks/      # Custom hooks
```

## Questions?

- Open an issue with tag `question`
- Join our [Discussions](https://github.com/yourusername/ai-vision-agent-pro/discussions)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help newcomers

Thank you for contributing! 🙏
