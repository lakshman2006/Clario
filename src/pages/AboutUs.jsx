import React from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../components/GlassCard';
import { 
  FaLinkedin, 
  FaGithub, 
  FaTwitter, 
  FaEnvelope,
  FaRocket,
  FaUsers,
  FaLightbulb,
  FaHeart,
  FaCode,
  FaPalette,
  FaChartLine,
  FaMobile
} from 'react-icons/fa';

const AboutUs = () => {
  const teamMembers = [
    {
      id: 1,
      name: 'Anjana',
      role: 'Frontend Developer',
      bio: 'Passionate about creating beautiful and intuitive user interfaces. Loves React and modern web technologies.',
      image: '/team/anjana.jpg', // Replace with your image path
      social: {
        linkedin: 'https://linkedin.com/in/anjana',
        github: 'https://github.com/anjana',
        twitter: 'https://twitter.com/anjana',
        email: 'anjana@clario.com'
      },
      skills: ['React', 'Javascript', 'Framer Motion',]
    },
    {
      id: 2,
      name: 'Banshika',
      role: 'Designer',
      bio: 'Expert in building scalable backend systems and implementing machine learning algorithms for personalized learning.',
      image: '/team/banshika.jpg', // Replace with your image path
      social: {
        linkedin: 'https://linkedin.com/in/banshika',
        github: 'https://github.com/banshika',
        twitter: 'https://twitter.com/banshika',
        email: 'banshika@clario.com'
      },
      skills: ['UI/UX Designing']
    },
    {
      id: 3,
      name: 'Lakshman',
      role: 'Team Leader ,Backend Development and ML integeration',
      bio: 'Enjoys solving complex problems and building end-to-end solutions. Passionate about clean code and best practices.',
      image: '/team/lakshman.jpg', // Replace with your image path
      social: {
        linkedin: 'https://linkedin.com/in/lakshman',
        github: 'https://github.com/lakshman',
        twitter: 'https://twitter.com/lakshman',
        email: 'lakshman@clario.com'
      },
      skills: ['Python', 'React', 'Node.js', 'AWS', 'DevOps']
    },
    {
      id: 4,
      name: 'Lohith',
      role: 'Database and Project Management',
      bio: 'Combines technical knowledge with educational expertise to create meaningful learning experiences for users.',
      image: '/team/lohith.jpg', // Replace with your image path
      social: {
        linkedin: 'https://linkedin.com/in/lohith',
        github: 'https://github.com/lohith',
        twitter: 'https://twitter.com/lohith',
        email: 'lohith@clario.com'
      },
      skills: ['Product Strategy', 'User Research', 'EdTech', 'Data Analysis']
    }
  ];

  const features = [
    {
      icon: <FaRocket className="feature-icon" />,
      title: 'Innovative Learning',
      description: 'We leverage cutting-edge technology to create personalized learning experiences that adapt to your needs.'
    },
    {
      icon: <FaUsers className="feature-icon" />,
      title: 'User-Centric Design',
      description: 'Every feature is designed with our users in mind, ensuring an intuitive and engaging experience.'
    },
    {
      icon: <FaLightbulb className="feature-icon" />,
      title: 'Smart Recommendations',
      description: 'Our AI algorithms analyze your learning patterns to recommend the perfect resources and schedules.'
    },
    {
      icon: <FaHeart className="feature-icon" />,
      title: 'Passionate Team',
      description: 'We are a team of lifelong learners dedicated to making education accessible and effective for everyone.'
    }
  ];

  const stats = [
    { number: '10,000+', label: 'Active Learners' },
    { number: '50,000+', label: 'Learning Hours' },
    { number: '5,000+', label: 'Schedules Created' },
    { number: '95%', label: 'User Satisfaction' }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="min-h-screen py-12"
    >
      <div className="container">
        {/* Hero Section */}
        <section className="text-center mb-16">
          <motion.h1 
            className="about-hero-title"
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6 }}
          >
            About CLARIO
          </motion.h1>
          <motion.p 
            className="about-hero-subtitle"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Empowering learners worldwide with personalized education paths and intelligent recommendations
          </motion.p>
        </section>


        {/* Team Section */}
        <section className="mb-16">
          <motion.h2 
            className="section-title text-center"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            Meet Our Team
          </motion.h2>
          <motion.p 
            className="section-subtitle text-center"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            A passionate team of developers, designers, and educators working together to revolutionize learning
          </motion.p>
          
          {/* Team Grid - 2x2 Layout */}
          <div className="team-grid">
            {/* First Row - First 2 Members */}
            <div className="team-row">
              {teamMembers.slice(0, 2).map((member, index) => (
                <motion.div
                  key={member.id}
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="team-member-wrapper"
                >
                  <GlassCard className="team-member-card">
                    {/* Member Image */}
                    <div className="member-image-container">
                      <div className="member-avatar">
                        <span className="avatar-text">
                          {member.name.split(' ').map(n => n[0]).join('')}
                        </span>
                      </div>
                    </div>

                    {/* Member Info */}
                    <div className="member-info">
                      <h3 className="member-name">{member.name}</h3>
                      <p className="member-role">{member.role}</p>
                      <p className="member-bio">{member.bio}</p>
                      
                      {/* Skills */}
                      <div className="member-skills">
                        {member.skills.map((skill, skillIndex) => (
                          <span key={skillIndex} className="skill-tag">{skill}</span>
                        ))}
                      </div>

                      {/* Social Links */}
                      <div className="member-social-links">
                        <a href={member.social.linkedin} className="social-link" aria-label="LinkedIn" target="_blank" rel="noopener noreferrer">
                          <FaLinkedin />
                        </a>
                        <a href={member.social.github} className="social-link" aria-label="GitHub" target="_blank" rel="noopener noreferrer">
                          <FaGithub />
                        </a>
                        <a href={member.social.twitter} className="social-link" aria-label="Twitter" target="_blank" rel="noopener noreferrer">
                          <FaTwitter />
                        </a>
                        <a href={`mailto:${member.social.email}`} className="social-link" aria-label="Email">
                          <FaEnvelope />
                        </a>
                      </div>
                    </div>
                  </GlassCard>
                </motion.div>
              ))}
            </div>

            {/* Second Row - Next 2 Members */}
            <div className="team-row">
              {teamMembers.slice(2, 4).map((member, index) => (
                <motion.div
                  key={member.id}
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: (index + 2) * 0.1 }}
                  className="team-member-wrapper"
                >
                  <GlassCard className="team-member-card">
                    {/* Member Image */}
                    <div className="member-image-container">
                      <div className="member-avatar">
                        <span className="avatar-text">
                          {member.name.split(' ').map(n => n[0]).join('')}
                        </span>
                      </div>
                    </div>

                    {/* Member Info */}
                    <div className="member-info">
                      <h3 className="member-name">{member.name}</h3>
                      <p className="member-role">{member.role}</p>
                      <p className="member-bio">{member.bio}</p>
                      
                      {/* Skills */}
                      <div className="member-skills">
                        {member.skills.map((skill, skillIndex) => (
                          <span key={skillIndex} className="skill-tag">{skill}</span>
                        ))}
                      </div>

                      {/* Social Links */}
                      <div className="member-social-links">
                        <a href={member.social.linkedin} className="social-link" aria-label="LinkedIn" target="_blank" rel="noopener noreferrer">
                          <FaLinkedin />
                        </a>
                        <a href={member.social.github} className="social-link" aria-label="GitHub" target="_blank" rel="noopener noreferrer">
                          <FaGithub />
                        </a>
                        <a href={member.social.twitter} className="social-link" aria-label="Twitter" target="_blank" rel="noopener noreferrer">
                          <FaTwitter />
                        </a>
                        <a href={`mailto:${member.social.email}`} className="social-link" aria-label="Email">
                          <FaEnvelope />
                        </a>
                      </div>
                    </div>
                  </GlassCard>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </motion.div>
  );
};

export default AboutUs;