#!/bin/bash

# Alzheimer's Memory Assistant - Complete Test Script
# This script starts all components needed for full functionality testing

set -e

echo "🚀 Starting Alzheimer's Memory Assistant Test Environment"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo -e "${YELLOW}Waiting for $service_name to be ready...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $service_name is ready!${NC}"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e "${RED}❌ $service_name failed to start within timeout${NC}"
    return 1
}

# Function to start backend server
start_backend() {
    echo -e "${BLUE}🔧 Starting Backend Server...${NC}"
    
    cd backend
    
    # Install system dependencies if needed
    echo -e "${YELLOW}Installing system dependencies...${NC}"
    pip3 install --user --quiet fastapi uvicorn pydantic 2>/dev/null || echo "Dependencies may already be installed"
    
    # Check if simple_main.py exists (simplified backend)
    if [ ! -f "simple_main.py" ]; then
        echo -e "${RED}❌ simple_main.py not found in backend directory${NC}"
        cd ..
        return 1
    fi
    
    # Start backend server in background
    echo -e "${YELLOW}Starting backend on localhost:8000...${NC}"
    python3 simple_main.py &
    BACKEND_PID=$!
    echo $BACKEND_PID > backend.pid
    
    cd ..
    
    # Wait for backend to be ready
    wait_for_service "http://localhost:8000/health" "Backend API"
}

# Function to start dashboard
start_dashboard() {
    echo -e "${BLUE}🖥️  Starting Dashboard...${NC}"
    
    cd dashboard-web
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing dashboard dependencies...${NC}"
        npm install --silent
    fi
    
    # Start dashboard in background
    echo -e "${YELLOW}Starting dashboard on localhost:3000...${NC}"
    npm run dev > dashboard.log 2>&1 &
    DASHBOARD_PID=$!
    echo $DASHBOARD_PID > dashboard.pid
    
    cd ..
    
    # Wait for dashboard to be ready
    sleep 5
    if check_port 3000; then
        echo -e "${GREEN}✅ Dashboard is ready at http://localhost:3000${NC}"
    elif check_port 3001; then
        echo -e "${GREEN}✅ Dashboard is ready at http://localhost:3001${NC}"
    else
        echo -e "${YELLOW}⚠️  Dashboard may still be starting...${NC}"
    fi
}

# Function to prepare mobile app
prepare_mobile() {
    echo -e "${BLUE}📱 Preparing Mobile App...${NC}"
    
    cd mobile-app
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing mobile app dependencies...${NC}"
        npm install --silent
    fi
    
    echo -e "${GREEN}✅ Mobile app is ready for Expo Go testing${NC}"
    echo -e "${YELLOW}📋 To test mobile app:${NC}"
    echo -e "   1. Install Expo Go on your phone"
    echo -e "   2. Run: cd mobile-app && npx expo start"
    echo -e "   3. Scan QR code with Expo Go app"
    
    cd ..
}

# Function to test API endpoints
test_api() {
    echo -e "${BLUE}🧪 Testing API Endpoints...${NC}"
    
    # Test health endpoint
    echo -e "${YELLOW}Testing health endpoint...${NC}"
    if curl -s http://localhost:8000/health | grep -q "healthy"; then
        echo -e "${GREEN}✅ Health endpoint working${NC}"
    else
        echo -e "${RED}❌ Health endpoint failed${NC}"
    fi
    
    # Test conversation endpoint
    echo -e "${YELLOW}Testing conversation endpoint...${NC}"
    RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/conversations \
        -H "Content-Type: application/json" \
        -d '{"content":"مرحبا كيف الحال؟","patient_id":1}')
    
    if echo "$RESPONSE" | grep -q "response"; then
        echo -e "${GREEN}✅ Conversation endpoint working${NC}"
        echo -e "${BLUE}Sample response: $(echo "$RESPONSE" | jq -r '.response' 2>/dev/null || echo "Response received")${NC}"
    else
        echo -e "${RED}❌ Conversation endpoint failed${NC}"
    fi
    
    # Test patient endpoint
    echo -e "${YELLOW}Testing patient endpoint...${NC}"
    if curl -s http://localhost:8000/api/v1/patients/1 | grep -q "name"; then
        echo -e "${GREEN}✅ Patient endpoint working${NC}"
    else
        echo -e "${RED}❌ Patient endpoint failed${NC}"
    fi
    
    # Test reminders endpoint
    echo -e "${YELLOW}Testing reminders endpoint...${NC}"
    if curl -s http://localhost:8000/api/v1/reminders/due | grep -q "\["; then
        echo -e "${GREEN}✅ Reminders endpoint working${NC}"
    else
        echo -e "${RED}❌ Reminders endpoint failed${NC}"
    fi
}

# Function to show system status
show_status() {
    echo -e "\n${BLUE}📊 System Status${NC}"
    echo "==================="
    
    # Backend status
    if check_port 8000; then
        echo -e "${GREEN}✅ Backend API: Running on http://localhost:8000${NC}"
    else
        echo -e "${RED}❌ Backend API: Not running${NC}"
    fi
    
    # Dashboard status
    if check_port 3000; then
        echo -e "${GREEN}✅ Dashboard: Running on http://localhost:3000${NC}"
    elif check_port 3001; then
        echo -e "${GREEN}✅ Dashboard: Running on http://localhost:3001${NC}"
    else
        echo -e "${RED}❌ Dashboard: Not running${NC}"
    fi
    
    # Mobile app status
    if [ -d "mobile-app/node_modules" ]; then
        echo -e "${GREEN}✅ Mobile App: Ready for testing${NC}"
    else
        echo -e "${YELLOW}⚠️  Mobile App: Dependencies not installed${NC}"
    fi
}

# Function to cleanup processes
cleanup() {
    echo -e "\n${YELLOW}🧹 Cleaning up processes...${NC}"
    
    # Kill backend
    if [ -f "backend/backend.pid" ]; then
        kill $(cat backend/backend.pid) 2>/dev/null || true
        rm backend/backend.pid
    fi
    
    # Kill dashboard
    if [ -f "dashboard-web/dashboard.pid" ]; then
        kill $(cat dashboard-web/dashboard.pid) 2>/dev/null || true
        rm dashboard-web/dashboard.pid
    fi
    
    echo -e "${GREEN}✅ Cleanup complete${NC}"
}

# Trap to cleanup on exit
trap cleanup EXIT

# Main execution
main() {
    case "${1:-start}" in
        "start")
            start_backend
            start_dashboard
            prepare_mobile
            test_api
            show_status
            
            echo -e "\n${GREEN}🎉 All services are running!${NC}"
            echo -e "${BLUE}📋 Quick Access:${NC}"
            echo -e "   • Backend API: http://localhost:8000"
            echo -e "   • Dashboard: http://localhost:3000 (or 3001)"
            echo -e "   • API Docs: http://localhost:8000/docs"
            echo -e "   • Health Check: http://localhost:8000/health"
            echo -e "\n${YELLOW}📱 To test mobile app:${NC}"
            echo -e "   cd mobile-app && npx expo start"
            echo -e "\n${YELLOW}Press Ctrl+C to stop all services${NC}"
            
            # Keep script running
            while true; do
                sleep 10
                if ! check_port 8000; then
                    echo -e "${RED}❌ Backend stopped unexpectedly${NC}"
                    break
                fi
            done
            ;;
        "stop")
            cleanup
            ;;
        "status")
            show_status
            ;;
        "test")
            test_api
            ;;
        *)
            echo "Usage: $0 {start|stop|status|test}"
            echo "  start  - Start all services (default)"
            echo "  stop   - Stop all services"
            echo "  status - Show service status"
            echo "  test   - Test API endpoints"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
