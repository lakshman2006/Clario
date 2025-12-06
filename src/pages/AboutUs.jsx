import React from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../components/GlassCard';
import { 
  FaLinkedin, 
  FaGithub, 
  FaInstagram,
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
      name: 'S.Lakshman',
      role: 'Backend Developer , Machine Learning , Team Lead',
      bio: '-',
      image: '/lakshman_profile.jpeg',
      social: {
        linkedin: '-',
        github: '-',
        instagram: '-',
        email: '-'
      },
      skills: ['Python, FastAPI, Machine Learning, Team Management']
    },
    {
      id: 2,
      name: 'Anjana M',
        role: 'Frontend Developer',
        bio: '-',
      image: '/anjana_profile.jpeg',
      social: {
        linkedin: 'https://www.linkedin.com/in/anjanamuthusamy?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app',
        github: 'https://github.com/Anjana2707',
        instagram: 'https://www.instagram.com/_an2an7_/',
        email: 'anjana.muthusamy27@gmail.com'
      },
      skills: ['HTML , CSS , JavaScript , React']
    },
    {
      id: 3,
      name: 'Banshika',
      role: 'Designer',
      bio: '-',
      image: '/banshika_profile.jpeg',
      social: {
        linkedin: 'https://www.linkedin.com/in/banshika-chowdhury-910568327/',
        github: 'https://github.com/bchowdhury07',
        instagram: 'https://www.instagram.com/banshikaa_07/',
        email: 'banshikachowdhuryb@gmail.com'
      },
      skills: ['Figma , Canva']
    },
    {
      id: 4,
      name: 'S.Lohith',
      role: 'Database and Git',
      bio: '-',
      image: '/lohith_profile.jpeg',
      social: {
        linkedin: '-',
        github: 'https://github.com/lohith032k',
        instagram: '-',
        email: 'lohith9j1@gmail.com'
      },
      skills: ['Database , Git']
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
          <h2 className="section-title">Meet Our Team</h2>
          <p className="section-subtitle">
            A passionate team of developers, designers, and educators working together to revolutionize learning
          </p>
          <div className="team-grid">
            {teamMembers.map((member, index) => (
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
                    <img 
                      src={member.image} 
                      alt={member.name}
                      className="member-image"
                      onError={(e) => {
                        e.target.src = '/default-avatar.png'; // Fallback image
                      }}
                    />
                    <div className="member-image-overlay"></div>
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
                    <div className="social-links">
                      <a href={member.social.linkedin} className="social-link" aria-label="LinkedIn">
                        <FaLinkedin />
                      </a>
                      <a href={member.social.github} className="social-link" aria-label="GitHub">
                        <FaGithub />
                      </a>
                      <a href={member.social.instagram} className="social-link" aria-label="Instagram">
                        <FaInstagram />
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
        </section>



        {/* Call to Action */}
        <section>
          <GlassCard className="cta-card">
            <div className="cta-content">
              <h2 className="cta-title">Ready to Start Your Learning Journey?</h2>
              <p className="cta-text">
                Join thousands of learners who have transformed their education with CLARIO
              </p>
              <div className="cta-buttons">
                <button className="btn-primary">Get Started</button>
                <button className="btn-secondary">Contact Us</button>
              </div>
            </div>
          </GlassCard>
        </section>
      </div>
    </motion.div>
  );
};

export default AboutUs;