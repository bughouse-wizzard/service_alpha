#!/usr/bin/env python3
import os
import re

def apply_change_to_file(filepath, old_code, new_code):
    """Apply a single change to a file"""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean up whitespace
    old_code_clean = '\n'.join([line.rstrip() for line in old_code.split('\n')])
    new_code_clean = '\n'.join([line.rstrip() for line in new_code.split('\n')])
    
    if old_code_clean in content:
        content = content.replace(old_code_clean, new_code_clean)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Applied change to {filepath}")
        return True
    else:
        print(f"Old code not found in {filepath}")
        return False

def main():
    base_dir = '/workspace/orkestrator-bot/dashboard/frontend'
    
    # 1. AdminTeams.tsx - fetchTeams
    teams_file = os.path.join(base_dir, 'src/pages/AdminTeams.tsx')
    old_fetch_teams = """useEffect(() => { fetchTeams(); }, []);

const fetchTeams = async () => {
  try {
    const token = localStorage.getItem('auth_token');
    const response = await axios.get('/api/admin/teams', {
      headers: { Authorization: `Bearer ${token}` }
    });
    setTeams(response.data);
  } catch (error) {
    console.error('Error fetching teams:', error);
  } finally {
    setLoading(false);
  }
};"""
    
    new_fetch_teams = """useEffect(() => { fetchTeams(); }, []);

const fetchTeams = async () => {
  setLoading(true);
  setError(null);
  try {
    const teamsData = await adminApi.get('/teams');
    setTeams(teamsData);
  } catch (error: any) {
    console.error('Error fetching teams:', error);
    toast.error(error.message || 'Failed to fetch teams');
  } finally {
    setLoading(false);
  }
};"""
    
    # First check if we need to add imports
    with open(teams_file, 'r', encoding='utf-8') as f:
        teams_content = f.read()
    
    if 'import { adminApi }' not in teams_content:
        # Add import at top
        lines = teams_content.split('\n')
        for i, line in enumerate(lines):
            if 'import axios' in line:
                lines.insert(i + 1, 'import { adminApi } from \'../api/adminApi\';')
                lines.insert(i + 2, 'import { toast } from \'react-toastify\';  // added import for toast notifications')
                break
        teams_content = '\n'.join(lines)
        with open(teams_file, 'w', encoding='utf-8') as f:
            f.write(teams_content)
        print("Added imports to AdminTeams.tsx")
    
    # Apply fetchTeams change
    apply_change_to_file(teams_file, old_fetch_teams, new_fetch_teams)
    
    # 2. AdminUsers.tsx - status badge
    users_file = os.path.join(base_dir, 'src/pages/AdminUsers.tsx')
    
    # Check if StatusBadge component exists, if not create it
    status_badge_file = os.path.join(base_dir, 'src/components/common/StatusBadge.tsx')
    if not os.path.exists(status_badge_file):
        os.makedirs(os.path.dirname(status_badge_file), exist_ok=True)
        with open(status_badge_file, 'w', encoding='utf-8') as f:
            f.write("""import React from 'react';

interface StatusBadgeProps {
  status: string;
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const statusLower = status.toLowerCase();
  let className = 'badge';
  
  if (statusLower.includes('active') || statusLower.includes('success')) {
    className += ' active';
  } else if (statusLower.includes('blocked') || statusLower.includes('failed') || statusLower.includes('error')) {
    className += ' blocked';
  } else if (statusLower.includes('pending') || statusLower.includes('warning')) {
    className += ' pending';
  }
  
  return (
    <span className={className}>
      {status}
    </span>
  );
};

export default StatusBadge;""")
        print("Created StatusBadge component")
    
    # Add import to AdminUsers.tsx if not present
    with open(users_file, 'r', encoding='utf-8') as f:
        users_content = f.read()
    
    if 'import StatusBadge' not in users_content:
        lines = users_content.split('\n')
        for i, line in enumerate(lines):
            if 'import React' in line:
                lines.insert(i + 1, 'import StatusBadge from \'../components/common/StatusBadge\';')
                break
        users_content = '\n'.join(lines)
        with open(users_file, 'w', encoding='utf-8') as f:
            f.write(users_content)
        print("Added StatusBadge import to AdminUsers.tsx")
    
    # Find and replace status display
    users_content = users_content.replace(
        '<td>{user.is_active ? \'Active\' : \'Blocked\'}</td>',
        '<td>\n  <StatusBadge status={user.is_active ? \'Active\' : \'Blocked\'} />\n</td>'
    )
    
    with open(users_file, 'w', encoding='utf-8') as f:
        f.write(users_content)
    print("Updated status display in AdminUsers.tsx")
    
    # 3. Create Breadcrumbs component
    breadcrumbs_file = os.path.join(base_dir, 'src/components/common/Breadcrumbs.tsx')
    if not os.path.exists(breadcrumbs_file):
        os.makedirs(os.path.dirname(breadcrumbs_file), exist_ok=True)
        with open(breadcrumbs_file, 'w', encoding='utf-8') as f:
            f.write("""import { useLocation, Link } from 'react-router-dom';

export const Breadcrumbs: React.FC = () => {
  const location = useLocation();
  const pathSegments = location.pathname.split('/').filter(seg => seg);

  // Map segments to display names (capitalize, etc.), skipping any IDs
  const crumbSegments = pathSegments.filter(seg =>
    // filter out UUIDs or numeric IDs
    !/^[0-9a-f-]{24,}$/.test(seg) && isNaN(Number(seg))
  );

  // Build cumulative path for each crumb link
  const breadcrumbs = crumbSegments.map((seg, idx) => {
    const name = seg.charAt(0).toUpperCase() + seg.slice(1);
    const to = '/' + pathSegments.slice(0, idx+1).join('/');
    const isLast = idx === crumbSegments.length - 1;
    return (
      <span key={idx}>
        {!isLast ? (
          <Link to={to} className="breadcrumb-link">{name}</Link>
        ) : (
          <span className="breadcrumb-current">{name}</span>
        )}
        {!isLast && <span className="breadcrumb-separator"> / </span>}
      </span>
    );
  });

  return (
    <nav className="breadcrumbs">
      {breadcrumbs}
    </nav>
  );
};""")
        print("Created Breadcrumbs component")
    
    # 4. Update AdminLayout.tsx to include breadcrumbs
    admin_layout_file = os.path.join(base_dir, 'src/components/AdminLayout.tsx')
    if os.path.exists(admin_layout_file):
        with open(admin_layout_file, 'r', encoding='utf-8') as f:
            layout_content = f.read()
        
        # Add Breadcrumbs import
        if 'import { Breadcrumbs }' not in layout_content:
            lines = layout_content.split('\n')
            for i, line in enumerate(lines):
                if 'import React' in line:
                    lines.insert(i + 1, 'import { Breadcrumbs } from \'./common/Breadcrumbs\';')
                    break
            layout_content = '\n'.join(lines)
        
        # Find where to add breadcrumbs (after header but before content)
        if '<div className="admin-content">' in layout_content:
            # Add breadcrumbs before admin-content
            layout_content = layout_content.replace(
                '<div className="admin-content">',
                '<Breadcrumbs />\n<div className="admin-content">'
            )
        
        with open(admin_layout_file, 'w', encoding='utf-8') as f:
            f.write(layout_content)
        print("Updated AdminLayout.tsx with breadcrumbs")
    
    print("\nAll manual changes applied!")

if __name__ == '__main__':
    main()