import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import {
  GitBranch,
  Plus,
  Search,
  Filter,
  Edit,
  Trash2,
  ExternalLink,
  CheckCircle,
  XCircle,
  GitPullRequest,
  Code,
  Globe,
  Lock,
  RefreshCw,
  Settings,
  Users
} from 'lucide-react';

interface Repository {
  id: string;
  project_id: string;
  repo_url: string;
  repo_name: string;
  branch: string;
  vcs_type: 'github' | 'gitlab' | 'gitea' | 'bitbucket';
  status: 'connected' | 'disconnected' | 'error';
  last_sync?: string;
  sync_status?: 'success' | 'failed' | 'pending';
  credentials_id?: string;
  created_at: string;
  updated_at: string;
  project_name?: string;
  team_name?: string;
}

interface Project {
  id: string;
  name: string;
  team_id: string;
  team_name?: string;
}

const AdminRepositories: React.FC = () => {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterProject, setFilterProject] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [syncingRepo, setSyncingRepo] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setError(null);
      
      // Try to fetch repositories from API
      // Note: API endpoint might not exist yet, so we'll handle the error
      const reposRes = await axios.get('/api/project-repos').catch(() => ({ data: [] }));
      
      // Try to fetch projects
      const projectsRes = await axios.get('/api/projects').catch(() => ({ data: [] }));

      // If no repositories from API, show empty state with helpful message
      if (!reposRes.data || reposRes.data.length === 0) {
        setRepositories([]);
        setProjects(projectsRes.data || []);
        setError('No repositories configured. Add your first repository to get started.');
      } else {
        setRepositories(reposRes.data);
        setProjects(projectsRes.data || []);
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
      setError('Unable to load repositories. The API endpoint may not be available yet.');
      setRepositories([]);
      setProjects([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSync = async (repoId: string) => {
    setSyncingRepo(repoId);
    try {
      await axios.post(`/api/project-repos/${repoId}/sync`);
      // Refresh data after sync
      await fetchData();
    } catch (error) {
      console.error('Sync failed:', error);
    } finally {
      setSyncingRepo(null);
    }
  };

  const handleDelete = async (repoId: string) => {
    if (window.confirm('Are you sure you want to delete this repository?')) {
      try {
        await axios.delete(`/api/project-repos/${repoId}`);
        // Refresh data after delete
        await fetchData();
      } catch (error) {
        console.error('Delete failed:', error);
      }
    }
  };

  const filteredRepos = repositories.filter(repo => {
    const matchesSearch = searchTerm === '' || 
      repo.repo_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      repo.repo_url.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (repo.project_name && repo.project_name.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesProject = filterProject === 'all' || repo.project_id === filterProject;
    const matchesStatus = filterStatus === 'all' || repo.status === filterStatus;
    
    return matchesSearch && matchesProject && matchesStatus;
  });

  const getVcsIcon = (vcsType: string) => {
    switch (vcsType) {
      case 'github': return <Globe size={16} />;
      case 'gitlab': return <GitBranch size={16} />;
      case 'gitea': return <Code size={16} />;
      case 'bitbucket': return <GitPullRequest size={16} />;
      default: return <Globe size={16} />;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected': return <CheckCircle size={16} className="text-green-500" />;
      case 'disconnected': return <XCircle size={16} className="text-gray-400" />;
      case 'error': return <XCircle size={16} className="text-red-500" />;
      default: return <XCircle size={16} className="text-gray-400" />;
    }
  };

  const getSyncStatusIcon = (syncStatus?: string) => {
    switch (syncStatus) {
      case 'success': return <CheckCircle size={16} className="text-green-500" />;
      case 'failed': return <XCircle size={16} className="text-red-500" />;
      case 'pending': return <RefreshCw size={16} className="text-yellow-500 animate-spin" />;
      default: return null;
    }
  };

  if (loading) {
    return (
      <div className="admin-repositories loading">
        <div className="loading-spinner"></div>
        <p>Loading repositories...</p>
      </div>
    );
  }

  return (
    <div className="admin-repositories">
      <div className="page-header">
        <div className="header-left">
          <h1>Repository Management</h1>
          <p className="subtitle">Manage version control system integrations</p>
        </div>
        <div className="header-right">
          <Link to="/admin/repositories/new" className="btn btn-primary">
            <Plus size={20} />
            Add Repository
          </Link>
        </div>
      </div>

      {error && (
        <div className="alert alert-info">
          <div className="alert-content">
            <Info size={20} />
            <div>
              <h4>No Repositories Found</h4>
              <p>{error}</p>
              <div className="alert-actions">
                <Link to="/admin/repositories/new" className="btn btn-sm btn-primary">
                  <Plus size={16} />
                  Add First Repository
                </Link>
                <button onClick={fetchData} className="btn btn-sm btn-outline">
                  <RefreshCw size={16} />
                  Retry
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {repositories.length > 0 && (
        <>
          <div className="filters-bar">
            <div className="search-box">
              <Search size={20} />
              <input
                type="text"
                placeholder="Search repositories..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            <div className="filter-group">
              <Filter size={20} />
              <select value={filterProject} onChange={(e) => setFilterProject(e.target.value)}>
                <option value="all">All Projects</option>
                {projects.map(project => (
                  <option key={project.id} value={project.id}>
                    {project.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <Filter size={20} />
              <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
                <option value="all">All Status</option>
                <option value="connected">Connected</option>
                <option value="disconnected">Disconnected</option>
                <option value="error">Error</option>
              </select>
            </div>

            <button onClick={fetchData} className="btn btn-outline">
              <RefreshCw size={20} />
              Refresh
            </button>
          </div>

          <div className="repositories-grid">
            {filteredRepos.map(repo => (
              <div key={repo.id} className="repository-card">
                <div className="card-header">
                  <div className="repo-info">
                    <div className="repo-icon">
                      {getVcsIcon(repo.vcs_type)}
                    </div>
                    <div>
                      <h3>{repo.repo_name}</h3>
                      <p className="repo-url">{repo.repo_url}</p>
                    </div>
                  </div>
                  <div className="card-actions">
                    <button
                      onClick={() => handleSync(repo.id)}
                      disabled={syncingRepo === repo.id}
                      className="btn btn-sm btn-outline"
                    >
                      {syncingRepo === repo.id ? (
                        <RefreshCw size={16} className="animate-spin" />
                      ) : (
                        <RefreshCw size={16} />
                      )}
                      Sync
                    </button>
                    <Link to={`/admin/repositories/${repo.id}/edit`} className="btn btn-sm btn-outline">
                      <Edit size={16} />
                    </Link>
                    <button
                      onClick={() => handleDelete(repo.id)}
                      className="btn btn-sm btn-outline btn-danger"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>

                <div className="card-content">
                  <div className="repo-details">
                    <div className="detail-item">
                      <span className="detail-label">Project:</span>
                      <span className="detail-value">{repo.project_name || 'N/A'}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Branch:</span>
                      <span className="detail-value">{repo.branch}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Status:</span>
                      <div className="detail-value status">
                        {getStatusIcon(repo.status)}
                        <span>{repo.status}</span>
                      </div>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Last Sync:</span>
                      <div className="detail-value">
                        {repo.last_sync ? new Date(repo.last_sync).toLocaleString() : 'Never'}
                        {repo.sync_status && (
                          <span className="sync-status">
                            {getSyncStatusIcon(repo.sync_status)}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="card-footer">
                  <a
                    href={repo.repo_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-sm btn-outline"
                  >
                    <ExternalLink size={16} />
                    Open Repository
                  </a>
                  <div className="footer-info">
                    <span className="created-at">
                      Added {new Date(repo.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredRepos.length === 0 && (
            <div className="empty-state">
              <Search size={48} />
              <h3>No repositories found</h3>
              <p>Try adjusting your search or filters</p>
            </div>
          )}
        </>
      )}

      {repositories.length === 0 && !error && (
        <div className="empty-state">
          <GitBranch size={48} />
          <h3>No repositories configured</h3>
          <p>Add your first repository to get started with version control integration</p>
          <Link to="/admin/repositories/new" className="btn btn-primary">
            <Plus size={20} />
            Add Repository
          </Link>
        </div>
      )}
    </div>
  );
};

// Add missing Info icon component
const Info = ({ size }: { size: number }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="10" />
    <line x1="12" y1="16" x2="12" y2="12" />
    <line x1="12" y1="8" x2="12.01" y2="8" />
  </svg>
);

export default AdminRepositories;