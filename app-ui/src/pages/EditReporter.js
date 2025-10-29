import ReporterForm from './ReporterForm';

const EditReporter = ({reporter}) => {
  return <ReporterForm key={`reporter-e-${reporter.id}`} reporter={reporter} />;
};

export default EditReporter;