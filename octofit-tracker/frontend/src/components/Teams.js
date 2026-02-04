import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const teamsUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
    const usersUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;
    console.log('Teams API endpoint:', teamsUrl);
    console.log('Users API endpoint:', usersUrl);

    Promise.all([
      fetch(teamsUrl).then(res => res.json()),
      fetch(usersUrl).then(res => res.json())
    ])
      .then(([teamsData, usersData]) => {
        console.log('Teams data fetched:', teamsData);
        console.log('Users data fetched:', usersData);
        
        const teamsArray = teamsData.results || teamsData;
        const usersArray = usersData.results || usersData;
        
        setTeams(Array.isArray(teamsArray) ? teamsArray : []);
        setUsers(Array.isArray(usersArray) ? usersArray : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const getMemberCount = (teamId) => {
    return users.filter(user => user.team_id === teamId).length;
  };

  if (loading) return (
    <div className="container mt-4">
      <div className="content-wrapper loading-container">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading teams...</p>
      </div>
    </div>
  );
  
  if (error) return (
    <div className="container mt-4">
      <div className="content-wrapper error-container">
        <p className="text-danger">Error: {error}</p>
      </div>
    </div>
  );

  return (
    <div className="container mt-4">
      <div className="content-wrapper">
        <h2 className="mb-4">Teams</h2>
        <div className="row">
        {teams.length > 0 ? (
          teams.map(team => (
            <div key={team.id} className="col-md-4 mb-4">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">{team.name}</h5>
                  <p className="card-text">{team.description}</p>
                  <ul className="list-group list-group-flush">
                    <li className="list-group-item">
                      <strong>Members:</strong> {getMemberCount(team._id || team.id)}
                    </li>
                    <li className="list-group-item">
                      <strong>Created:</strong> {new Date(team.created_at).toLocaleDateString()}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <p className="text-center">No teams found</p>
          </div>
        )}
        </div>
      </div>
    </div>
  );
}

export default Teams;
