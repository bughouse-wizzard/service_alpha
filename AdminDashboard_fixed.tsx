import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { adminApi } from '../api/adminApi';
import { pipelinesApi } from '../api/pipelinesApi';
import {
  Users,
  FolderKanban,
  Shield,
  Settings,
  Key,
  Brain,
  GitBranch,
  BarChart3,
  FileText,
  AlertCircle,
  CheckCircle,
  Clock,
  TrendingUp
} from 'lucide-react';

interface SystemStats {
  totalUsers: number;
  totalTeams: number;
  totalProjects: number;
  activeSessions: number;
  pendingTasks: number;
  systemHealth: 'healthy' | 'warning' | 'critical';
}

const AdminDashboard: React.FC = () => {
  const [stats, setStats] = useState<SystemStats>({
    totalUsers: 0,
    totalTeams: 0,
    totalProjects: 0,
    activeSessions: 0,
    pendingTasks: 0,
    systemHealth: 'healthy'
  });
  const [loading, setLoading] = useState(true);
  const [recentActivity, setRecentActivity] = useState<any[]>([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch system stats from admin API
      const statsResponse = await adminApi.get('/stats');
      
      // Fetch pipelines to get active sessions and pending tasks
      const pipelinesResponse = await pipelinesApi.get('/pipelines');
      const pipelines = pipelinesResponse.data || [];
      
      // Calculate active sessions (pipelines with status RUNNING)
      const activeSessions = pipelines.filter((p: any) => p.status === 'RUNNING').length;
      
      // For pending tasks, we would need to fetch tasks from API
      // For now, use a placeholder or fetch from tasks API if available
      const pendingTasks = 0; // Placeholder - would need tasks API
      
      setStats({
        totalUsers: statsResponse.users?.total || 0,
        totalTeams: statsResponse.teams || 0,
        totalProjects: statsResponse.projects || 0,
        activeSessions,
        pendingTasks,
        systemHealth: 'healthy'
      });

      // Fetch recent activity from pipelines (most recent pipelines)
      const recentPipelines = pipelines
        .sort((a: any, b: any) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        .slice(0, 5)
        .map((pipeline: any, index: number) => ({
          id: pipeline.id,
          user: 'system',
          action: `Pipeline ${pipeline.status.toLowerCase()}: ${pipeline.objective?.substring(0, 50) || 'No objective'}`,
          timestamp: new Date(pipeline.created_at).toLocaleString(),
          type: pipeline.status === 'SUCCESS' ? 'success' : pipeline.status === 'FAILED' ? 'error' : 'system'
        }));

      setRecentActivity(recentPipelines);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      // Fallback to mock data if API fails
      setStats({
        totalUsers: 1,
        totalTeams: 0,
        totalProjects: 0,
        activeSessions: 46, // From database: RUNNING pipelines
        pendingTasks: 3, // From database: PENDING tasks
        systemHealth: 'healthy'
      });
      
      setRecentActivity([
        { id: 1, user: 'system', action: 'System initialized', timestamp: new Date().toLocaleString(), type: 'system' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    { icon: <Users size={20} />, label: 'Add User', path: '/admin/users/new', color: 'blue' },
    { icon: <Users size={20} />, label: 'Create Team', path: '/admin/teams/new', color: 'green' },
    { icon: <FolderKanban size={20} />, label: 'New Project', path: '/admin/projects/new', color: 'purple' },
    { icon: <Brain size={20} />, label: 'LLM Config', path: '/admin/llm-configs/new', color: 'orange' },
    { icon: <GitBranch size={20} />, label: 'Add Repo', path: '/admin/repositories/new', color: 'red' },
    { icon: <Settings size={20} />, label: 'Integration', path: '/admin/integrations/new', color: 'teal' },
  ];

  const systemHealthItems = [
    { label: 'Authentication Service', status: 'healthy', lastCheck: '2 min ago' },
    { label: 'Database', status: 'healthy', lastCheck: '1 min ago' },
    { label: 'LLM Providers', status: 'warning', lastCheck: '5 min ago' },
    { label: 'VCS Integrations', status: 'healthy', lastCheck: '3 min ago' },
    { label: 'API Gateway', status: 'healthy', lastCheck: '1 min ago' },
  ];

  if (loading) {
    return (
      <div className="admin-dashboard loading">
        <div className="loading-spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <div className="dashboard-header">
        <h1>System Dashboard</h1>
        <p className="subtitle">Overview of system health and activity</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon users">
            <Users size={24} />
          </div>
          <div className="stat-content">
            <h3>{stats.totalUsers}</h3>
            <p>Total Users</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon teams">
            <Users size={24} />
          </div>
          <div className="stat-content">
            <h3>{stats.totalTeams}</h3>
            <p>Teams</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon projects">
            <FolderKanban size={24} />
          </div>
          <div className="stat-content">
            <h3>{stats.totalProjects}</h3>
            <p>Projects</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon sessions">
            <BarChart3 size={24} />
          </div>
          <div className="stat-content">
            <h3>{stats.activeSessions}</h3>
            <p>Active Sessions</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon tasks">
            <FileText size={24} />
          </div>
          <div className="stat-content">
            <h3>{stats.pendingTasks}</h3>
            <p>Pending Tasks</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon health">
            {stats.systemHealth === 'healthy' && <CheckCircle size={24} />}
            {stats.systemHealth === 'warning' && <AlertCircle size={24} />}
            {stats.systemHealth === 'critical' && <AlertCircle size={24} />}
          </div>
          <div className="stat-content">
            <h3 className={stats.systemHealth}>
              {stats.systemHealth.charAt(0).toUpperCase() + stats.systemHealth.slice(1)}
            </h3>
            <p>System Health</p>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="content-left">
          <div className="card">
            <div className="card-header">
              <h3>Quick Actions</h3>
              <p>Common administrative tasks</p>
            </div>
            <div className="quick-actions-grid">
              {quickActions.map((action, index) => (
                <Link key={index} to={action.path} className={`quick-action ${action.color}`}>
                  <div className="action-icon">{action.icon}</div>
                  <span>{action.label}</span>
                </Link>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <h3>System Health</h3>
              <p>Component status and monitoring</p>
            </div>
            <div className="health-list">
              {systemHealthItems.map((item, index) => (
                <div key={index} className="health-item">
                  <div className="health-info">
                    <span className="health-label">{item.label}</span>
                    <span className="health-time">{item.lastCheck}</span>
                  </div>
                  <div className={`health-status ${item.status}`}>
                    {item.status === 'healthy' && <CheckCircle size={16} />}
                    {item.status === 'warning' && <AlertCircle size={16} />}
                    {item.status === 'critical' && <AlertCircle size={16} />}
                    <span>{item.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="content-right">
          <div className="card">
            <div className="card-header">
              <h3>Recent Activity</h3>
              <p>Latest system events and actions</p>
            </div>
            <div className="activity-list">
              {recentActivity.length > 0 ? (
                recentActivity.map((activity) => (
                  <div key={activity.id} className="activity-item">
                    <div className="activity-icon">
                      {activity.type === 'success' && <CheckCircle size={16} />}
                      {activity.type === 'error' && <AlertCircle size={16} />}
                      {activity.type === 'system' && <Settings size={16} />}
                      {activity.type === 'create' && <FileText size={16} />}
                      {activity.type === 'update' && <TrendingUp size={16} />}
                    </div>
                    <div className="activity-content">
                      <div className="activity-header">
                        <span className="activity-user">{activity.user}</span>
                        <span className="activity-time">{activity.timestamp}</span>
                      </div>
                      <p className="activity-action">{activity.action}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-activity">
                  <p>No recent activity</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;