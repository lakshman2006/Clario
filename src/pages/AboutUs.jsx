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
      name: 'Alex Johnson',
      role: 'Frontend Developer & UI/UX Designer',
      bio: 'Passionate about creating beautiful and intuitive user interfaces. Loves React and modern web technologies.',
      image: '/team/alex-johnson.jpg', // Replace with your image path
      social: {
        linkedin: 'https://linkedin.com/in/alexjohnson',
        github: 'https://github.com/alexjohnson',
        twitter: 'https://twitter.com/alexjohnson',
        email: 'alex@clario.com'
      },
      skills: ['React', 'TypeScript', 'Framer Motion', 'UI/UX Design']
    },
    {
      id: 2,
      name: 'Sarah Chen',
      role: 'Backend Developer & AI Specialist',
      bio: 'Expert in building scalable backend systems and implementing machine learning algorithms for personalized learning.',
      image: '/team/sarah-chen.jpg', // Replace with your image path
      social: {
        linkedin: 'https://linkedin.com/in/sarahchen',
        github: 'https://github.com/sarahchen',
        twitter: 'https://twitter.com/sarahchen',
        email: 'sarah@clario.com'
      },
      skills: ['Node.js', 'Python', 'Machine Learning', 'Database Design']
    },
    {
      id: 3,
      name: 'Mike Rodriguez',
      role: 'Full Stack Developer',
      bio: 'Enjoys solving complex problems and building end-to-end solutions. Passionate about clean code and best practices.',
      image: '/team/mike-rodriguez.jpg', // Replace with your image path
      social: {
        linkedin: 'https://linkedin.com/in/mikerodriguez',
        github: 'https://github.com/mikerodriguez',
        twitter: 'https://twitter.com/mikerodriguez',
        email: 'mike@clario.com'
      },
      skills: ['JavaScript', 'React', 'Node.js', 'AWS', 'DevOps']
    },
    {
      id: 4,
      name: 'Emily Davis',
      role: 'Product Manager & Learning Strategist',
      bio: 'Combines technical knowledge with educational expertise to create meaningful learning experiences for users.',
      image: '/team/emily-davis.jpg', // Replace with your image path
      social: {
        linkedin: 'https://linkedin.com/in/emilydavis',
        github: 'https://github.com/emilydavis',
        twitter: 'https://twitter.com/emilydavis',
        email: 'emily@clario.com'
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

        {/* Mission Section */}
        <section className="mb-16">
          <GlassCard className="mission-card">
            <div className="mission-content">
              <h2 className="mission-title">Our Mission</h2>
              <p className="mission-text">
                At CLARIO, we believe that everyone deserves access to personalized, effective learning experiences. 
                Our platform combines artificial intelligence with educational expertise to create custom learning paths 
                that adapt to your goals, schedule, and learning style. We're committed to making quality education 
                accessible to all.
              </p>
            </div>
          </GlassCard>
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
                      <a href={member.social.twitter} className="social-link" aria-label="Twitter">
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